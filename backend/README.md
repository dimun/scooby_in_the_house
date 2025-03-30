# Scooby In The House - Backend

This is the backend service for Scooby In The House, a real estate scraper for Colombian properties.

## Setup

1. Create a virtual environment and install dependencies:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

3. Set up the PostgreSQL database:
   - Make sure PostgreSQL is installed and running
   - Create a database named `scooby_db` (or update the `.env` file)

4. Run migrations:
   ```
   alembic upgrade head
   ```

5. Start the development server:
   ```
   uvicorn app.main:app --reload
   ```

## Database Migrations

To create a new migration after making changes to the database models:

```
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## API Endpoints

- `GET /api/v1/properties` - Get properties with optional filtering
- `POST /api/v1/scrape` - Start a scraping job for properties in a city/region
- `GET /api/v1/properties/stats` - Get statistics about properties in the database

The complete API documentation is available at `/docs` when the server is running.

## Web Scraping

The application can scrape real estate listings from fincaraiz.com.co. To start a scraping job:

```python
from app.services.scraper_service import scrape_properties
from app.db import SessionLocal

db = SessionLocal()
try:
    # Scrape properties in Manizales, Caldas
    scrape_properties("manizales", "caldas", max_pages=5, db=db)
finally:
    db.close()
```

Or via API:

```bash
curl -X POST "http://localhost:8000/api/v1/scrape" \
     -H "Content-Type: application/json" \
     -d '{"city": "manizales", "region": "caldas", "max_pages": 5}'
``` 