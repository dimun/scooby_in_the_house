# Scooby In The House

A real estate scraper for Colombian properties, built with FastAPI and React.

## Project Structure

```
scooby_in_the_house/
├── backend/             # FastAPI backend
│   ├── app/             # API source code
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core modules
│   │   ├── db/          # Database models and configuration
│   │   ├── models/      # Pydantic models
│   │   ├── schemas/     # Schema definitions
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utility functions
│   ├── tests/           # Test suite
│   └── pyproject.toml   # Python project configuration and dependencies
│
├── frontend/            # React frontend
│   ├── public/          # Static files
│   └── src/             # React source code
│       ├── api/         # API client
│       ├── components/  # React components
│       ├── hooks/       # Custom React hooks
│       ├── pages/       # Page components
│       └── types/       # TypeScript type definitions
│
└── docker-compose.yml   # Docker Compose for PostgreSQL database
```

## Getting Started

### Prerequisites

1. Install uv, the fast Python package installer and resolver:
   ```
   # Using the official installer script (Linux/macOS)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On macOS with Homebrew
   brew install uv

   # On Windows with PowerShell
   irm https://astral.sh/uv/install.ps1 | iex
   ```

2. Install Docker and Docker Compose (optional, for containerized setup)

### Docker Setup (Recommended)

The easiest way to get started is to use Docker:

1. Start the PostgreSQL database:
   ```
   docker-compose up -d
   ```

2. Run the backend:
   ```
   cd backend
   docker-compose up -d
   ```

   Or run all services together:
   ```
   docker-compose -f docker-compose.full.yml up -d
   ```

See [README-docker.md](README-docker.md) for more details on Docker setup.

### Manual Setup

#### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment and install dependencies using uv:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

4. Set up the PostgreSQL database:
   - Make sure PostgreSQL is installed and running
   - Create a database named `scooby_db` (or update the `.env` file)

5. Run migrations:
   ```
   alembic upgrade head
   ```

6. Start the development server:
   ```
   uvicorn app.main:app --reload
   ```

7. The API will be available at http://localhost:8000
   - API documentation: http://localhost:8000/docs

#### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. The application will be available at http://localhost:5173

## Technologies

### Backend
- FastAPI: Modern, fast web framework for building APIs with Python
- uv: Fast Python package installer and resolver
- Pydantic: Data validation using Python type annotations
- SQLAlchemy: SQL toolkit and ORM
- Beautiful Soup: Web scraping library

### Frontend
- React: UI library
- TypeScript: Static type checking
- Vite: Build tool and development server
- React Router: Routing library
- Axios: HTTP client
- React Query: Data fetching and caching

### Infrastructure
- PostgreSQL: Relational database
- Docker: Containerization platform
- Docker Compose: Multi-container Docker applications 