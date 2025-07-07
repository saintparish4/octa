# OCTA Backend

A FastAPI-based backend for geospatial and network analysis.

## Features

- **Spatial Data Management** - CRUD operations with PostgreSQL (latitude/longitude coordinates)
- **Network Analysis** - Graph operations with Neo4j  
- **Background Task Processing** - Async jobs with Celery
- **Caching Layer** - Redis for performance optimization
- **RESTful API** - Clean endpoints with automatic documentation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start services with Docker:
```bash
docker-compose up -d
```

3. Run the application:
```bash
python main.py
```

## API Endpoints

- `GET /api/v1/` - API root
- `POST /api/v1/spatial/spatial-data/` - Create spatial data
- `GET /api/v1/spatial/spatial-data/` - Get all spatial data
- `GET /api/v1/spatial/spatial-data/{id}` - Get spatial data by ID
- `GET /api/v1/spatial/spatial-data/within/` - Get spatial data within coordinate bounds
- `POST /api/v1/network/network/shortest-path/` - Find shortest path
- `GET /api/v1/network/network/centrality/` - Calculate centrality
- `POST /api/v1/tasks/process-dataset/` - Start dataset processing
- `POST /api/v1/tasks/calculate-network-metrics/` - Start network analysis
- `GET /api/v1/tasks/task-status/{task_id}` - Check task progress
- `GET /api/v1/tasks/spatial-statistics/` - Get spatial statistics
- `GET /api/v1/tasks/detect-hotspots/` - Detect spatial hotspots

## Environment Variables

Create a `.env` file with:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=networkpass
REDIS_URL=redis://localhost:6379
```

## Background Tasks

The application supports background task processing with Celery:

1. **Start Celery Worker:**
```bash
celery -A app.core.celery_app worker --loglevel=info
```

2. **Monitor Tasks:**
```bash
celery -A app.core.celery_app flower
```

## Database Schema

The application uses PostgreSQL with a simplified spatial data model:

### Spatial Data Table
- `id` - Primary key
- `name` - Location name (VARCHAR)
- `latitude` - Latitude coordinate (FLOAT)
- `longitude` - Longitude coordinate (FLOAT)
- `properties` - Additional data (JSONB)
- `created_at` - Timestamp

This approach uses standard PostgreSQL without requiring PostGIS extensions, making it easier to deploy and maintain.

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation. 