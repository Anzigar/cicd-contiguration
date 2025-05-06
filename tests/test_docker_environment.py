"""
Tests for Docker environment and container configuration.

This module tests the Docker-related functionality and environment setup.
"""
import os
import subprocess
from typing import List, Dict, Any
import pytest


def check_docker_command_exists() -> bool:
    """
    Check if Docker command is available on the system.
    
    Returns:
        bool: True if Docker is available, False otherwise.
    """
    try:
        subprocess.run(
            ["docker", "--version"], 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


@pytest.mark.skipif(
    not check_docker_command_exists(),
    reason="Docker not available on this system"
)
def test_dockerfile_exists() -> None:
    """
    Test that the Dockerfile exists and has the expected content.
    """
    dockerfile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Dockerfile")
    assert os.path.exists(dockerfile_path), "Dockerfile does not exist"
    
    with open(dockerfile_path, "r") as f:
        content = f.read()
    
    # Check for critical Dockerfile components
    assert "FROM python" in content, "Dockerfile should use Python base image"
    assert "WORKDIR /app" in content, "Dockerfile should set working directory"
    assert "COPY requirements.txt" in content, "Dockerfile should copy requirements"
    assert "EXPOSE" in content, "Dockerfile should expose port"


@pytest.mark.skipif(
    not check_docker_command_exists(),
    reason="Docker not available on this system"
)
def test_entrypoint_script() -> None:
    """
    Test that the entrypoint script exists and has necessary components.
    """
    entrypoint_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "entrypoint.sh"
    )
    assert os.path.exists(entrypoint_path), "entrypoint.sh does not exist"
    
    with open(entrypoint_path, "r") as f:
        content = f.read()
    
    # Check for critical entrypoint components
    assert "#!/bin/bash" in content, "Entrypoint should be a bash script"
    assert "python" in content, "Entrypoint should run Python"
    assert "uvicorn" in content, "Entrypoint should start uvicorn server"


def test_environment_variables_in_compose() -> None:
    """
    Test that the docker-compose.yml file properly sets environment variables.
    """
    compose_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "docker-compose.yml"
    )
    
    if not os.path.exists(compose_path):
        pytest.skip("docker-compose.yml does not exist")
    
    with open(compose_path, "r") as f:
        content = f.read().lower()
    
    # Check for environment configurations
    assert "environment:" in content, "docker-compose should set environment variables"
    
    # Check if port mapping is correctly set up
    assert "ports:" in content, "docker-compose should map ports"