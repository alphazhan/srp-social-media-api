FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl git gcc g++ libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependencies and install
COPY pyproject.toml uv.lock ./
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install --upgrade pip && \
    uv sync

# Copy ML application source code (after deps installed)
COPY . .

# Expose FastAPI port
EXPOSE 8001

CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]


