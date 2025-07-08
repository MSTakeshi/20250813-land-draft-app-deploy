FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

# Install build dependencies for asyncpg and other packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Cargo/Maturin to use writable directories
ENV CARGO_HOME=/tmp/cargo_home
ENV CARGO_TARGET_DIR=/tmp/cargo_target

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]