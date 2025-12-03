FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Go (for Go code execution)
RUN curl -L https://go.dev/dl/go1.21.5.linux-amd64.tar.gz | tar -C /usr/local -xzf - && \
    ln -s /usr/local/go/bin/go /usr/local/bin/go

# Install Java JDK (for Java code execution)
RUN apt-get update && apt-get install -y \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy backend files
COPY . /app/
WORKDIR /app

# Install Python dependencies
RUN uv sync

# Expose port
EXPOSE 8000

# Set Python path
ENV PYTHONPATH=/app

# Run migrations and then start the application
CMD ["sh", "-c", "uv run python migrations.py && uv run uvicorn main:socket_app --host 0.0.0.0 --port 8000"]

