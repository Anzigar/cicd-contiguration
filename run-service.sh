#!/bin/bash
# Script to run the FastAPI service in different environments
# Usage: ./run-service.sh [local|docker|docker-compose]

set -e

# Default environment variables
export PORT=${PORT:-8000}
export HOST=${HOST:-"0.0.0.0"}
export ENVIRONMENT=${ENVIRONMENT:-"development"}

function show_help() {
    echo "FastAPI Service Runner"
    echo "---------------------"
    echo "Usage: ./run-service.sh [command]"
    echo ""
    echo "Commands:"
    echo "  local              Run the service locally using Python's venv"
    echo "  docker             Build and run using Docker"
    echo "  docker-compose     Run using Docker Compose"
    echo "  test               Run the tests"
    echo "  lint               Lint the code using flake8"
    echo "  format             Format the code using black"
    echo "  help               Show this help message"
    echo ""
}

function setup_venv() {
    echo "Setting up virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual environment set up successfully."
}

function run_local() {
    if [ ! -d "venv" ]; then
        setup_venv
    else
        source venv/bin/activate
    fi
    
    echo "Starting FastAPI service locally on $HOST:$PORT in $ENVIRONMENT mode..."
    if [ "$ENVIRONMENT" = "development" ]; then
        uvicorn main:app --host $HOST --port $PORT --reload
    else
        uvicorn main:app --host $HOST --port $PORT
    fi
}

function run_docker() {
    echo "Building Docker image..."
    docker build -t fastapi-app .
    
    echo "Running container on port $PORT..."
    docker run -p $PORT:$PORT \
        -e PORT=$PORT \
        -e HOST=$HOST \
        -e ENVIRONMENT=$ENVIRONMENT \
        fastapi-app
}

function run_docker_compose() {
    if [ ! -f "docker-compose.yml" ]; then
        echo "docker-compose.yml not found. Creating one..."
        cat > docker-compose.yml << EOF
version: '3.8'

services:
  api:
    build: .
    ports:
      - "${PORT}:${PORT}"
    environment:
      - PORT=${PORT}
      - HOST=${HOST}
      - ENVIRONMENT=${ENVIRONMENT}
    restart: unless-stopped
EOF
    fi
    
    echo "Running service with Docker Compose..."
    docker-compose up --build
}

function run_tests() {
    echo "Running tests..."
    if [ ! -d "venv" ]; then
        setup_venv
    else
        source venv/bin/activate
    fi
    
    python -m pytest
}

function run_lint() {
    echo "Linting code..."
    if [ ! -d "venv" ]; then
        setup_venv
    else
        source venv/bin/activate
    fi
    
    flake8 .
}

function run_format() {
    echo "Formatting code with black..."
    if [ ! -d "venv" ]; then
        setup_venv
    else
        source venv/bin/activate
    fi
    
    black .
}

# Check command
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

# Execute command
case "$1" in
    "local")
        run_local
        ;;
    "docker")
        run_docker
        ;;
    "docker-compose")
        run_docker_compose
        ;;
    "test")
        run_tests
        ;;
    "lint")
        run_lint
        ;;
    "format")
        run_format
        ;;
    "help")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac