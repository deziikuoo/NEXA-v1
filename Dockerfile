# Multi-stage build for better efficiency
FROM node:18-alpine AS frontend-builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --no-audit --no-fund

# Copy source code
COPY . .

# Build the React app
RUN npm run build

# Python runtime stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built React app from the frontend stage
COPY --from=frontend-builder /app/build ./build

# Copy Python source code
COPY app_fastapi.py .
COPY start.py .

# Expose port
EXPOSE ${PORT:-8000}

# Start the application
CMD ["python3", "start.py"] 