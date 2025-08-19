# Cat and Dog Image Classifier

A machine learning web application that can identify whether an uploaded image contains a cat or a dog.

## Overview

This application uses a TensorFlow/Keras deep learning model to classify images as either cats or dogs. The model was trained on a dataset of cat and dog images and achieves good accuracy on most clear photos of these animals.

The web interface allows users to upload their own images directly through a browser and get instant predictions.

## Features

- Simple, user-friendly web interface
- Real-time image classification
- Supports common image formats (JPG, PNG, GIF)
- Containerized for easy deployment

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
docker build -t catdog-classifier .
```

3. **Run the Docker container**

```bash
docker run -p 5000:5000 catdog-classifier
```

4. **Access the application**

Open your web browser and navigate to: [http://localhost:5000](http://localhost:5000)

## Deploying to AlmaLinux Server

1. **Transfer project files to your server**

2. **Build and run the Docker container on the server**

```bash
docker build -t catdog-classifier .
docker run -d -p 80:5000 --restart unless-stopped --name catdog-app catdog-classifier
```

3. **Access the deployed application**

Open your web browser and navigate to: http://[your-server-ip]

## Using the Interface

1. Open the application in your web browser
2. Click "Choose File" or drag and drop an image into the upload area
3. Click the "Classify Image" button
4. View the prediction result (Cat or Dog)

## Technical Details

- **Framework**: Flask web framework
- **Machine Learning**: TensorFlow/Keras
- **Model Architecture**: Convolutional Neural Network (CNN)
- **Image Processing**: All images are resized to 224x224 pixels before classification

## Known Issues and Limitations

- The classifier works best with clear, well-lit photos where the animal is the primary subject
- Performance may be reduced with:
  - Images containing both cats and dogs
  - Poor lighting conditions
  - Unusual angles or partially visible animals
  - Exotic breeds not well-represented in the training data
- Processing large images may take a few seconds
- The model is optimized for cats and dogs only and may give unpredictable results for other animals or objects

## Troubleshooting

- If you encounter memory issues, ensure your Docker instance has at least 2GB RAM allocated
- For image upload problems, verify that your image is in a supported format (JPG, PNG, GIF)
- If the application fails to start, check Docker logs: `docker logs catdog-app`

## License

[Your License Information]

## Credits

- TensorFlow for the machine learning framework
- Flask for the web application framework
