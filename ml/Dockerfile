# Use official Python slim image (more stable for ML deps than alpine)
FROM python:3.13-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal build dependencies
RUN apt-get update && apt-get install -y \
    curl git gcc g++ libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./

# Create virtual env and sync dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install --upgrade pip && \
    uv sync

# Copy the source code
COPY . .

# Expose port
EXPOSE 8000

# Launch FastAPI app using Uvicorn via uv
CMD [".venv/bin/uvicorn", "ml.main:app", "--host", "0.0.0.0", "--port", "8000"]
