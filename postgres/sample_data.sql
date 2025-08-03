-- Sample data for routes
INSERT INTO routes (name, path) VALUES
('Route A', ST_GeogFromText('LINESTRING(-122.389977 37.616299, -118.407997 33.941589)')),
('Route B', ST_GeogFromText('LINESTRING(-118.407997 33.941589, -115.152333 36.080056)'));

-- Sample data for airports
INSERT INTO airports (code, name, location, elevation) VALUES
('SFO', 'San Francisco International Airport', ST_GeogFromText('POINT(-122.389977 37.616299)'), 13),
('LAX', 'Los Angeles International Airport', ST_GeogFromText('POINT(-118.407997 33.941589)'), 125);

-- Sample data for notams
INSERT INTO notams (route_id, message, effective_from, effective_to, area) VALUES
(1, 'Temporary airspace restriction', NOW(), NOW() + INTERVAL '7 days', ST_GeogFromText('POLYGON((-122.5 37.6, -122.3 37.6, -122.3 37.7, -122.5 37.7, -122.5 37.6))'));
