#!/bin/bash
set -e

echo "Python environment information:"
python --version

echo "Starting the application..."
echo "Using port: ${PORT:-8000}"
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}