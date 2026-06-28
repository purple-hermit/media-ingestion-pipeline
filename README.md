# Automated Media Ingestion Pipeline

A lightweight, Dockerized watch-folder service that intercepts dropped audio or video assets and transcodes them into a standardized production format (H.264/AAC `.mp4`) using FFmpeg.

It includes a hardware monitoring logger that tracks raw CPU frequencies (`/proc/cpuinfo`) in real-time.

### Features
* **Drop-and-Forget Automation:** An infinite-loop daemon that processes files synchronously and cleans up source pool on success.
* **Preserved Naming Integrity:** Prepends a timestamped `LOT` prefix to filename for production tracking.
* **Hardware Aware Logging:** Streams real-time pipeline status, exact Python error tracebacks, live system metrics directly to the terminal and a persistent log file.
* **Optimized Containerization:** Built on a hardened `python:3.11-slim` Docker image to minimize resource footprint, eliminate host environment dependencies and graceful shutdowns via direct signal handling.


## Usage

### 1. Build the Docker image

```bash
docker build -t media-pipeline .
```

### 2. Run the container

```bash
docker run -d \
  --name pipeline-worker \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  media-pipeline
```

### 3. View container logs

```bash
docker logs -f pipeline-worker
```