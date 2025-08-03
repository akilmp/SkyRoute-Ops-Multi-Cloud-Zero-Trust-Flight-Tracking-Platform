package ingest

import (
	"context"
	"sync"
)

// FlightRepository persists flight messages to storage.
type FlightRepository interface {
	InsertFlight(ctx context.Context, f FlightMessage) error
}

// Publisher publishes flight messages to downstream systems.
type Publisher interface {
	Publish(ctx context.Context, f FlightMessage) error
}

// Processor handles incoming messages, ensuring deduplication before
// persisting and publishing them.
type Processor struct {
	repo      FlightRepository
	publisher Publisher
	mu        sync.Mutex
	seen      map[string]struct{}
}

// NewProcessor creates a new Processor.
func NewProcessor(repo FlightRepository, publisher Publisher) *Processor {
	return &Processor{
		repo:      repo,
		publisher: publisher,
		seen:      make(map[string]struct{}),
	}
}

// Process deduplicates and forwards a flight message.
func (p *Processor) Process(ctx context.Context, f FlightMessage) error {
	p.mu.Lock()
	if _, exists := p.seen[f.ID]; exists {
		p.mu.Unlock()
		return nil
	}
	p.seen[f.ID] = struct{}{}
	p.mu.Unlock()

	if err := p.repo.InsertFlight(ctx, f); err != nil {
		return err
	}
	if err := p.publisher.Publish(ctx, f); err != nil {
		return err
	}
	return nil
}
