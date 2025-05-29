FROM python:3.13-slim as fastapi-base-image

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.base.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.base.txt
