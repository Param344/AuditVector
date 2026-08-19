# Multi-stage Dockerfile for AuditVector on Google Cloud Run
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY backend /app/backend
COPY frontend /app/frontend
COPY integritylab /app/integritylab
COPY run_audit.sh /app/

RUN chmod +x /app/run_audit.sh

EXPOSE 8080

# Run FastAPI backend via uvicorn
CMD ["uvicorn", "backend.api.server:app", "--host", "0.0.0.0", "--port", "8080"]
