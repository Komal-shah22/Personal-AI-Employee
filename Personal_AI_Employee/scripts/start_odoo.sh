#!/bin/bash

# Odoo Quick Start Script for Mac/Linux

echo "============================================================"
echo "ODOO 17 COMMUNITY EDITION - QUICK START"
echo "============================================================"
echo ""

# Check if Docker is running
echo "[1/4] Checking Docker..."
if ! docker ps >/dev/null 2>&1; then
    echo ""
    echo "ERROR: Docker is not running!"
    echo ""
    echo "Please start Docker Desktop and wait for it to be ready."
    echo "Then run this script again."
    echo ""
    exit 1
fi
echo "    ✓ Docker is running!"
echo ""

# Navigate to project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# Pull images
echo "[2/4] Pulling Docker images (this may take a few minutes)..."
if ! docker-compose pull; then
    echo "    ✗ Failed to pull images"
    exit 1
fi
echo "    ✓ Images pulled successfully!"
echo ""

# Start containers
echo "[3/4] Starting Odoo and PostgreSQL containers..."
if ! docker-compose up -d; then
    echo "    ✗ Failed to start containers"
    exit 1
fi
echo "    ✓ Containers started successfully!"
echo ""

# Wait for Odoo to be ready
echo "[4/4] Waiting for Odoo to be ready (30 seconds)..."
sleep 30
echo "    ✓ Odoo should be ready!"
echo ""

# Check container status
echo "Container Status:"
docker-compose ps
echo ""

echo "============================================================"
echo "ODOO IS READY!"
echo "============================================================"
echo ""
echo "Access Odoo at: http://localhost:8069"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:8069 in your browser"
echo "2. Create a database (see scripts/setup_odoo.md for details)"
echo "3. Enable modules: Invoicing, Accounting, Contacts"
echo "4. Create API user for external access"
echo ""
echo "To view logs: docker-compose logs -f odoo"
echo "To stop Odoo: docker-compose down"
echo ""
