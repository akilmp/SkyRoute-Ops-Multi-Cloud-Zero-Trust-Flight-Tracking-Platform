package stream

import (
	"context"

	"github.com/skyroute/ingest-api/internal/ingest"
)

// Consumer pulls flight messages from a streaming source.
type Consumer interface {
	Consume(ctx context.Context, out chan<- ingest.FlightMessage) error
}
