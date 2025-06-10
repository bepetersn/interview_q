# Deployment Guide

This document outlines how to build and deploy the container image for the Interview Questions application.

## Build the Docker image

```bash
docker build -t interview-q .
```

## Push to your registry

Tag the image and push it to your preferred container registry. Example using GitHub Container Registry:

```bash
docker tag interview-q ghcr.io/<your-username>/interview-q:latest
docker push ghcr.io/<your-username>/interview-q:latest
```

## Run the container

After pushing the image, pull and run it on your server:

```bash
docker run -d -p 8000:8000 ghcr.io/<your-username>/interview-q:latest
```

The Django API will be available on port `8000` and the built React files are bundled within the same container.
