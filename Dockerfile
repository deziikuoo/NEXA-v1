# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy package files
COPY package*.json ./

# Install Node.js dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the React app
RUN npm run build

# Expose port
EXPOSE $PORT

# Start the application
CMD ["python3", "-m", "uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "$PORT"] 