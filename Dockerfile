# Using a lightweight python image based on Debian
FROM python:3.11-slim
# No .pyc(python cache files) and no buffer for print statements so we get a live log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install FFmpeg and cleans up the package manager cache in one RUN statement
RUN apt-get update && \
apt-get install -y --no-install-recommends ffmpeg && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
# Setting up the working directory in the container
WORKDIR /app
# Copies pipeline script from host machine to the container's app directory
COPY pipeline.py .
# Setting up the internal file structure needed to run the script
RUN mkdir -p input output logs
# Defining the command that runs when the container starts
CMD ["python", "pipeline.py"]