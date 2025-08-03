package ingest

import (
	"context"
	"sync"
	"testing"
)

type mockRepo struct {
	mu  sync.Mutex
	ids []string
}

func (m *mockRepo) InsertFlight(ctx context.Context, f FlightMessage) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.ids = append(m.ids, f.ID)
	return nil
}

type mockPublisher struct {
	mu  sync.Mutex
	ids []string
}

func (m *mockPublisher) Publish(ctx context.Context, f FlightMessage) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.ids = append(m.ids, f.ID)
	return nil
}

func TestProcessorDedup(t *testing.T) {
	repo := &mockRepo{}
	pub := &mockPublisher{}
	proc := NewProcessor(repo, pub)

	ctx := context.Background()
	msgs := []FlightMessage{
		{ID: "1"},
		{ID: "1"},
		{ID: "2"},
		{ID: "2"},
	}

	for _, m := range msgs {
		if err := proc.Process(ctx, m); err != nil {
			t.Fatalf("process: %v", err)
		}
	}

	if len(repo.ids) != 2 {
		t.Fatalf("expected 2 inserts, got %d", len(repo.ids))
	}
	if len(pub.ids) != 2 {
		t.Fatalf("expected 2 publishes, got %d", len(pub.ids))
	}
}
