# Use Python slim image (good for uv + FastAPI + SQLite)
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system deps (for bcrypt, sqlite, etc.)
RUN apt-get update && apt-get install -y \
    curl git build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy only dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Create virtual environment and sync dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install --upgrade pip && \
    uv sync

# Copy application source code
COPY app ./app
COPY app/main.py main.py
COPY app/config.py config.py

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
