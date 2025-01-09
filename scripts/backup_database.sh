#!/bin/bash

# backup_database.sh - Script to backup the database

set -e  # Exit immediately if a command exits with a non-zero status

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Define backup directory and filename
BACKUP_DIR="backups"
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Backing up the database to $BACKUP_FILE..."

# Assuming you're using PostgreSQL; adjust for your database
pg_dump $DATABASE_URL > $BACKUP_FILE

echo "Database backup completed successfully."
