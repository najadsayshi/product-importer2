FROM python:3.11-slim

# Install system packages + supervisor
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend + frontend
COPY backend/app /app/app
COPY frontend /app/frontend

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Start supervisor (which runs FastAPI + Celery worker)
CMD ["/usr/bin/supervisord"]
