package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"os"
	"time"

	gcppubsub "cloud.google.com/go/pubsub"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	awskinesis "github.com/aws/aws-sdk-go-v2/service/kinesis"
)

func main() {
	rate := flag.Int("rate", 1, "messages per second")
	random := flag.Float64("random", 0, "randomness factor for delay (0-1)")
	flag.Parse()

	ctx := context.Background()
	provider := getenv("CLOUD_PROVIDER", "AWS")
	rand.Seed(time.Now().UnixNano())

	var publish func(context.Context, []byte) error
	switch provider {
	case "AWS":
		cfg, err := config.LoadDefaultConfig(ctx)
		if err != nil {
			log.Fatalf("aws config: %v", err)
		}
		client := awskinesis.NewFromConfig(cfg)
		streamName := getenv("KINESIS_STREAM", "flights")
		publish = func(ctx context.Context, data []byte) error {
			_, err := client.PutRecord(ctx, &awskinesis.PutRecordInput{
				StreamName:   aws.String(streamName),
				PartitionKey: aws.String(fmt.Sprintf("pk-%d", rand.Int())),
				Data:         data,
			})
			return err
		}
	case "GCP":
		projectID := getenv("GCP_PROJECT", "project")
		topicID := getenv("PUBSUB_TOPIC", "flights")
		psClient, err := gcppubsub.NewClient(ctx, projectID)
		if err != nil {
			log.Fatalf("pubsub client: %v", err)
		}
		defer psClient.Close()
		topic := psClient.Topic(topicID)
		publish = func(ctx context.Context, data []byte) error {
			res := topic.Publish(ctx, &gcppubsub.Message{Data: data})
			_, err := res.Get(ctx)
			return err
		}
	default:
		log.Fatalf("unsupported cloud provider: %s", provider)
	}

	interval := time.Second / time.Duration(*rate)
	for {
		msg := make([]byte, 14)
		rand.Read(msg)
		if err := publish(ctx, msg); err != nil {
			log.Printf("publish: %v", err)
		}
		delay := interval
		if *random > 0 {
			jitter := time.Duration(rand.Float64() * (*random) * float64(interval))
			delay += jitter
		}
		time.Sleep(delay)
	}
}

func getenv(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}
