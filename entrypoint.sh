#!/bin/bash
set -e

echo "Python environment information:"
python --version

# Ensure dependencies are installed
echo "Checking for dependencies..."
pip install -r requirements.txt

echo "Starting the application..."
echo "Using port: ${PORT:-8000}"
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}