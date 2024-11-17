# Dockerfile to build the gatorTicketMaster executable using Python 3.10.14 on Debian Buster Slim

# Stage 1: Build Stage
FROM python:3.10.14-slim-buster AS build

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build the executable using the Makefile
RUN make

# Stage 2: Create a minimal image with the executable
FROM debian:buster-slim

# Set the working directory
WORKDIR /app

# Copy the executable from the build stage
COPY --from=build /app/gatorTicketMaster /app/gatorTicketMaster

# Set the entrypoint to the executable (optional)
ENTRYPOINT ["/app/gatorTicketMaster"]
