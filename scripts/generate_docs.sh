#!/bin/bash

# generate_docs.sh - Script to generate documentation

set -e  # Exit immediately if a command exits with a non-zero status

echo "Generating documentation..."

# Generate API documentation
# Assuming you have a docs folder with Sphinx setup
sphinx-build -b html docs/ docs/_build/html

echo "Documentation generated successfully at docs/_build/html."
