package storage

import (
	"context"
	"database/sql"

	_ "github.com/ClickHouse/clickhouse-go/v2"
	"github.com/skyroute/ingest-api/internal/ingest"
)

// ClickHouseRepository stores flights in ClickHouse.
type ClickHouseRepository struct {
	db *sql.DB
}

// NewClickHouseRepository creates a ClickHouse-backed repository.
func NewClickHouseRepository(db *sql.DB) *ClickHouseRepository {
	return &ClickHouseRepository{db: db}
}

// InsertFlight inserts a flight record into ClickHouse.
func (r *ClickHouseRepository) InsertFlight(ctx context.Context, f ingest.FlightMessage) error {
	_, err := r.db.ExecContext(ctx, "INSERT INTO flights (id, data) VALUES (?, ?)", f.ID, f.Data)
	return err
}
