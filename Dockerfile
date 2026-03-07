FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY database ./database
COPY ingestion ./ingestion
COPY ml ./ml

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# On container start: create tables and generate synthetic data.
CMD bash -c "python database/migrate.py && python ingestion/generate_data.py && echo '✅ Database ready with sample data.'"

