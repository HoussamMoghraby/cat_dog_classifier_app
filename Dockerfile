# Use a Python base with system libraries needed for OpenCV and YOLO
FROM python:3.9-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies required for OpenCV and YOLO
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Separate dependency layer
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app source
COPY . .

# Tell Docker which port the app listens on
EXPOSE 6000

# Run via Gunicorn (1 worker per CPU core is typical; start simple)
CMD ["gunicorn", "-b", "0.0.0.0:6000", "-w", "2", "app:app"]
