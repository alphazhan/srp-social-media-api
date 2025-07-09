FROM python:3.13-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    curl git build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install --upgrade pip && \
    uv sync

# Copy source code
COPY app ./app
COPY app/main.py main.py
COPY app/config.py config.py

EXPOSE 8000

CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
