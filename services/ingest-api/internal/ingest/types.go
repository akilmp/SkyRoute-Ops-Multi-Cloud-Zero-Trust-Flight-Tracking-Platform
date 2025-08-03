package ingest

// FlightMessage represents a single flight telemetry message.
type FlightMessage struct {
	ID   string
	Data []byte
}
