# Use Python as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (Node.js + build tools)
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential curl     && curl -fsSL https://deb.nodesource.com/setup_18.x | bash -     && apt-get install -y nodejs     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel     && pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies & build
COPY frontend ./frontend
RUN cd frontend && npm install && npm run build

# Copy backend code
COPY app ./app
COPY sample_data ./sample_data
COPY scripts ./scripts

# Copy frontend build into backend static dir
RUN mkdir -p /app/app/static     && cp -r frontend/build/* /app/app/static/

# Expose port
EXPOSE 8000

# Start backend (FastAPI/Flask)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
