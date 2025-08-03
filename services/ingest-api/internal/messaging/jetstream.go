package messaging

import (
	"context"

	"github.com/nats-io/nats.go"
	"github.com/skyroute/ingest-api/internal/ingest"
)

// JetStreamPublisher publishes messages to a NATS JetStream subject.
type JetStreamPublisher struct {
	js      nats.JetStreamContext
	subject string
}

// NewJetStreamPublisher creates a JetStream publisher.
func NewJetStreamPublisher(js nats.JetStreamContext, subject string) *JetStreamPublisher {
	return &JetStreamPublisher{js: js, subject: subject}
}

// Publish sends a flight message to JetStream.
func (p *JetStreamPublisher) Publish(ctx context.Context, f ingest.FlightMessage) error {
	_, err := p.js.Publish(p.subject, f.Data, nats.Context(ctx))
	return err
}
