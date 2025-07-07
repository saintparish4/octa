# Database Setup

This directory contains the database initialization for the Octa project.

## Quick Start

```bash
# Start the database
docker-compose up -d postgres
```

## Schema

The `spatial_data` table stores geographic points with properties:

- `id` - Unique identifier
- `name` - Point name
- `geom` - Geographic coordinates (PostGIS)
- `properties` - JSON metadata
- `created_at` - Creation timestamp

## Connection Details

- **Host**: localhost:5432
- **Database**: octa_db
- **Username**: octauser
- **Password**: octapass 