package stream

import (
	"context"

	"github.com/aws/aws-sdk-go-v2/service/kinesis"
	"github.com/skyroute/ingest-api/internal/ingest"
)

// KinesisConsumer consumes messages from AWS Kinesis.
type KinesisConsumer struct {
	client *kinesis.Client
	stream string
}

// NewKinesisConsumer creates a Kinesis consumer.
func NewKinesisConsumer(client *kinesis.Client, stream string) *KinesisConsumer {
	return &KinesisConsumer{client: client, stream: stream}
}

// Consume reads messages from Kinesis. This is a placeholder implementation.
func (c *KinesisConsumer) Consume(ctx context.Context, out chan<- ingest.FlightMessage) error {
	<-ctx.Done()
	return ctx.Err()
}
