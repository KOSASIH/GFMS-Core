#!/bin/bash

# deploy.sh - Deployment script for the GFMS application

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

echo "Deployment completed successfully."
