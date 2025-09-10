FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY app ./app
COPY scripts ./scripts
COPY sample_data ./sample_data
COPY frontend/build ./frontend/build
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
