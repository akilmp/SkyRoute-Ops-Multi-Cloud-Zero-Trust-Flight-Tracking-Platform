# PostgreSQL Setup

This directory contains SQL scripts for initializing the database schema and loading sample data for development or testing.

## Initialization

1. Connect to your PostgreSQL database.
2. Run the initialization script:
   ```sh
   psql -U <username> -d <database> -f init.sql
   ```

## Sample Data

Load sample routes, airports, and NOTAMs data using:
```sh
psql -U <username> -d <database> -f sample_data.sql
```

## Migrations

Place future schema changes in separate SQL files and apply them in order. A common pattern is to prefix migration files with incremental numbers, e.g. `001_add_index.sql`, `002_add_new_table.sql`:
```sh
psql -U <username> -d <database> -f migrations/001_add_index.sql
```

Ensure the `postgis` extension is installed before running migrations that depend on spatial types.
