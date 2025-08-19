# Example (CPU):
FROM python:3.10-slim
RUN pip install --no-cache-dir "torch==2.5.*" "ultralytics==8.*" gunicorn flask

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies required for OpenCV and YOLO with better error handling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    libfontconfig1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Separate dependency layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Tell Docker which port the app listens on
EXPOSE 5000

# Run via Gunicorn (1 worker per CPU core is typical; start simple)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app:app"]