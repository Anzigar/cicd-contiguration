"""Test configuration for the entire test suite.

This module contains shared fixtures and configuration for all tests.
"""
import os
import pytest
from typing import Generator, Dict, Any


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """
    Set up the test environment with required environment variables.
    
    This fixture runs once per test session and sets up necessary
    environment variables for testing.
    
    Yields:
        None
    """
    # Save original environment variables
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ["ENVIRONMENT"] = "test"
    os.environ["PORT"] = "8000"
    os.environ["HOST"] = "0.0.0.0"
    
    # Execute tests
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_request_data() -> Dict[str, Any]:
    """
    Provide sample request data for testing.
    
    Returns:
        Dict[str, Any]: A dictionary with sample request data.
    """
    return {
        "name": "Test Project",
        "description": "A test project for CI/CD",
        "version": "1.0.0",
        "environment": "test"
    }