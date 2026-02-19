FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    chromium \
    chromium-driver \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install PM2 globally
RUN npm install -g pm2

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Install Node dependencies
RUN npm install

# Expose port (if needed for health checks)
EXPOSE 8080

# Start command
CMD ["pm2-runtime", "start", "ecosystem.config.js"]
