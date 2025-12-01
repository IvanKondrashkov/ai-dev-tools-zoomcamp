FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install Python dependencies using uv (install dependencies directly, not as package)
RUN uv pip install --system "Django>=5.0.0,<6.0.0" "psycopg2-binary>=2.9.0" "python-dotenv>=1.0.0"

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run migrations (schema already created by SQL scripts, but Django needs to track migrations)
# and start server
CMD ["sh", "-c", "python manage.py migrate --fake-initial && python manage.py runserver 0.0.0.0:8000"]

