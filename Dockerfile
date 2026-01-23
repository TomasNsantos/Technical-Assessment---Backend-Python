FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-c", "print('Container Python OK')"]

ENV PYTHONPATH=/

HEALTHCHECK --interval=10s --timeout=2s --retries=5 \
  CMD curl -f http://localhost:8000/health || exit 1

