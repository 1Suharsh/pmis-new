FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install only what’s needed
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel     && pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app ./app
COPY scripts ./scripts
# sample_data only if needed:
# COPY sample_data ./sample_data

# Expose port
EXPOSE 8000

# Run with multiple workers for better concurrency
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]
