"""
Tests for the FastAPI application main module.

This module contains tests for the endpoints defined in main.py.
"""

import os
from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Returns:
        TestClient: A TestClient instance for making requests to the app.
    """
    return TestClient(app)


def test_root_endpoint(client: TestClient) -> None:
    """
    Test the root endpoint of the application.

    Args:
        client: TestClient fixture to make requests.
    """
    response = client.get("/")
    assert response.status_code == 200
    data: Dict[str, Any] = response.json()
    assert "message" in data
    assert data["message"] == "Hello World"
    assert "status" in data
    assert data["status"] == "Running"


def test_health_endpoint(client: TestClient) -> None:
    """
    Test the health check endpoint.

    Args:
        client: TestClient fixture to make requests.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_environment_variables() -> None:
    """
    Test that environment variables are properly handled.
    """
    from main import app

    # Test default values
    assert app.title == "CI/CD Configuration API"
    assert app.version == "0.1.0"

    # Test environment variable access
    env_var = os.environ.get("ENVIRONMENT", "development")
    assert isinstance(env_var, str)
