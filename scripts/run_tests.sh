#!/bin/bash

# run_tests.sh - Script to run automated tests

set -e  # Exit immediately if a command exits with a non-zero status

echo "Running tests..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Run tests
pytest tests/

echo "All tests completed."
