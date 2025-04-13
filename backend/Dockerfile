FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install uv

# Copy requirements
COPY pyproject.toml ./

# Install dependencies with pip directly to ensure they're in PATH
RUN pip install -e .
RUN pip install uvicorn fastapi

# Copy application code
COPY . .

# Create an .env file if it doesn't exist
RUN if [ ! -f .env ]; then cp .env.example .env || echo "No .env.example found"; fi

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["/app/scripts/start.sh"] 