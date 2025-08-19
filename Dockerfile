# Use a slim Python base
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system deps (optional but useful for building wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Separate dependency layer
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app source
COPY . .

# Tell Docker which port the app listens on
EXPOSE 5000

# Run via Gunicorn (1 worker per CPU core is typical; start simple)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app:app"]
