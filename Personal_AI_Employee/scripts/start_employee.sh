#!/bin/bash

# Start All AI Employee Services
# This script starts all watchers and orchestrator using PM2

echo "=========================================="
echo "Starting Personal AI Employee Services"
echo "=========================================="
echo ""

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "PM2 not found. Installing PM2..."
    npm install -g pm2
    echo "PM2 installed successfully!"
    echo ""
fi

# Navigate to project directory
cd "$(dirname "$0")"

# Start all services using ecosystem config
echo "Starting all services..."
pm2 start ecosystem.config.js

# Save PM2 process list
echo ""
echo "Saving PM2 configuration..."
pm2 save

# Setup PM2 to start on system boot
echo ""
echo "Setting up PM2 startup..."
pm2 startup

echo ""
echo "=========================================="
echo "All services started successfully!"
echo "=========================================="
echo ""

# Show status
pm2 status

echo ""
echo "Useful commands:"
echo "  pm2 status          - Show all services status"
echo "  pm2 logs            - View all logs"
echo "  pm2 logs gmail-watcher - View specific service logs"
echo "  pm2 restart all     - Restart all services"
echo "  pm2 stop all        - Stop all services"
echo "  pm2 monit           - Monitor services in real-time"
echo ""
