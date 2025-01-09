#!/bin/bash

# seed_database.sh - Script to seed the database with initial data

set -e  # Exit immediately if a command exits with a non-zero status

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Run the seed data script
echo "Seeding the database with initial data..."

python src/database/seed_data.py

echo "Database seeding completed successfully."
