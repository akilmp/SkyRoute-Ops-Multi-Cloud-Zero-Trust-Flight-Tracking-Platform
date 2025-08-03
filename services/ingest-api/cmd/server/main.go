package main

import (
	"context"
	"database/sql"
	"log"
	"os"

	gcppubsub "cloud.google.com/go/pubsub"
	"github.com/aws/aws-sdk-go-v2/config"
	awskinesis "github.com/aws/aws-sdk-go-v2/service/kinesis"
	"github.com/nats-io/nats.go"

	"github.com/skyroute/ingest-api/internal/ingest"
	"github.com/skyroute/ingest-api/internal/messaging"
	"github.com/skyroute/ingest-api/internal/storage"
	"github.com/skyroute/ingest-api/internal/stream"
)

func main() {
	ctx := context.Background()

	provider := os.Getenv("CLOUD_PROVIDER")
	clickhouseDSN := getenv("CLICKHOUSE_DSN", "tcp://clickhouse:9000?database=default")
	natsURL := getenv("NATS_URL", nats.DefaultURL)
	natsSubject := getenv("NATS_SUBJECT", "flights")

	db, err := sql.Open("clickhouse", clickhouseDSN)
	if err != nil {
		log.Fatalf("clickhouse connect: %v", err)
	}
	defer db.Close()

	nc, err := nats.Connect(natsURL)
	if err != nil {
		log.Fatalf("nats connect: %v", err)
	}
	defer nc.Drain()

	js, err := nc.JetStream()
	if err != nil {
		log.Fatalf("jetstream: %v", err)
	}

	repo := storage.NewClickHouseRepository(db)
	publisher := messaging.NewJetStreamPublisher(js, natsSubject)
	processor := ingest.NewProcessor(repo, publisher)

	msgCh := make(chan ingest.FlightMessage)

	var consumer stream.Consumer
	switch provider {
	case "AWS":
		cfg, err := config.LoadDefaultConfig(ctx)
		if err != nil {
			log.Fatalf("aws config: %v", err)
		}
		client := awskinesis.NewFromConfig(cfg)
		streamName := getenv("KINESIS_STREAM", "flights")
		consumer = stream.NewKinesisConsumer(client, streamName)
	case "GCP":
		projectID := getenv("GCP_PROJECT", "project")
		subID := getenv("PUBSUB_SUBSCRIPTION", "flights")
		psClient, err := gcppubsub.NewClient(ctx, projectID)
		if err != nil {
			log.Fatalf("pubsub client: %v", err)
		}
		defer psClient.Close()
		sub := psClient.Subscription(subID)
		consumer = stream.NewPubSubConsumer(sub)
	default:
		log.Fatalf("unsupported cloud provider: %s", provider)
	}

	go func() {
		if err := consumer.Consume(ctx, msgCh); err != nil {
			log.Fatalf("consume: %v", err)
		}
	}()

	for msg := range msgCh {
		if err := processor.Process(ctx, msg); err != nil {
			log.Printf("process: %v", err)
		}
	}
}

func getenv(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}
