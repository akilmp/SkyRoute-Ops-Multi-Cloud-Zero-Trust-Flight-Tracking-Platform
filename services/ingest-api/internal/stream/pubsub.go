package stream

import (
	"context"

	"cloud.google.com/go/pubsub"
	"github.com/skyroute/ingest-api/internal/ingest"
)

// PubSubConsumer consumes messages from Google Pub/Sub.
type PubSubConsumer struct {
	sub *pubsub.Subscription
}

// NewPubSubConsumer creates a Pub/Sub consumer.
func NewPubSubConsumer(sub *pubsub.Subscription) *PubSubConsumer {
	return &PubSubConsumer{sub: sub}
}

// Consume receives messages from Pub/Sub and forwards them to the channel.
func (c *PubSubConsumer) Consume(ctx context.Context, out chan<- ingest.FlightMessage) error {
	return c.sub.Receive(ctx, func(ctx context.Context, msg *pubsub.Message) {
		out <- ingest.FlightMessage{ID: msg.ID, Data: msg.Data}
		msg.Ack()
	})
}
