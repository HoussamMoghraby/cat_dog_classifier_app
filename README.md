# Cat and Dog Object Detector

<img width="635" height="572" alt="image" src="https://github.com/user-attachments/assets/1615ba57-8a27-4c98-a205-57f3c1019bf5" />

A machine learning web application that can detect and highlight cats and dogs in uploaded images.

## Overview

This application uses YOLOv8, a state-of-the-art object detection model, to identify and locate cats and dogs in images. The model can detect multiple animals in a single image and will highlight them with color-coded bounding boxes (green for cats, red for dogs).

The web interface allows users to upload their own images directly through a browser and get visual results showing detected animals.

## Features

- Simple, user-friendly web interface
- Real-time object detection with visual highlighting
- Detects and distinguishes between cats and dogs
- Supports common image formats (JPG, PNG, GIF)
- Containerized for easy deployment
- Can detect multiple animals in a single image


## Setup Instructions

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine
- At least 2GB of free RAM for running the application

### Running Locally with Docker

1. **Clone this repository**

```bash
git clone [your-repository-url]
cd ZakaAI-ML-Prod
```

2. **Build the Docker image**

```bash
docker build -t catdog-detector .
```

3. **Run the Docker container**

```bash
docker run -p 6000:6000 catdog-detector
```

4. **Access the application**

Open your web browser and navigate to: [http://localhost:6000](http://localhost:6000)

## Deploying to AlmaLinux Server

1. **Transfer project files to your server**

2. **Build and run the Docker container on the server**

```bash
docker build -t catdog-detector .
docker run -d -p 80:6000 --restart unless-stopped --name catdog-detector-app catdog-detector
```

3. **Access the deployed application**

Open your web browser and navigate to: http://[your-server-ip]

## Using the Interface

1. Open the application in your web browser
2. Click "Choose File" or drag and drop an image into the upload area
3. Click the "Detect Objects" button
4. View the processed image with highlighted cats (green boxes) and dogs (red boxes)
5. See a summary of detected animals below the image

[screen-capture (1).webm](https://github.com/user-attachments/assets/698c33fc-028d-4f0c-b45f-7e2b42bbf05b)

## Technical Details

- **Framework**: Flask web framework
- **Machine Learning**: YOLOv8 (You Only Look Once) object detection
- **Model Architecture**: Real-time object detection network
- **Detection Performance**: Can detect 80 different object classes, with special highlighting for cats and dogs

## Known Issues and Limitations

- The detector works best with clear, well-lit photos
- Performance may be reduced with:
  - Poor lighting conditions
  - Very small animals in the image
  - Unusual angles or partially visible animals
  - Heavy occlusion (objects blocking the view of the animals)
- Processing large images may take a few seconds
- While the model can detect 80 different object classes, only cats and dogs are highlighted with colored boxes
- Detection confidence may vary based on the clarity and positioning of animals in the image

## Troubleshooting

- If you encounter memory issues, ensure your Docker instance has at least 2GB RAM allocated
- For image upload problems, verify that your image is in a supported format (JPG, PNG, GIF)
- If the application fails to start, check Docker logs: `docker logs catdog-detector-app`


## Credits

- Ultralytics for the YOLOv8 implementation
- Flask for the web application framework
- OpenCV for image processing
