#!/bin/bash

# Stop All AI Employee Services

echo "=========================================="
echo "Stopping Personal AI Employee Services"
echo "=========================================="
echo ""

# Stop all PM2 processes
pm2 stop all

echo ""
echo "All services stopped."
echo ""

# Show status
pm2 status

echo ""
echo "To restart services, run: ./scripts/start_employee.sh"
echo ""
