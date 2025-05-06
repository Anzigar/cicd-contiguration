"""
Tests for CI/CD workflow configuration.

This module tests the GitHub Actions workflow configuration for CI/CD.
"""
import os
import yaml
from typing import Dict, Any, List
import pytest


def test_github_workflow_exists() -> None:
    """
    Test that the GitHub Actions workflow file exists.
    """
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".github/workflows/cicd.yml"
    )
    assert os.path.exists(workflow_path), "GitHub Actions workflow file does not exist"


def test_github_workflow_configuration() -> None:
    """
    Test that the GitHub Actions workflow has the expected structure and jobs.
    """
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".github/workflows/cicd.yml"
    )
    
    if not os.path.exists(workflow_path):
        pytest.skip("GitHub Actions workflow file does not exist")
    
    with open(workflow_path, "r") as f:
        workflow_config = yaml.safe_load(f)
    
    # Check that the workflow has a name
    assert "name" in workflow_config, "Workflow should have a name"
    
    # Check that the workflow has jobs
    assert "jobs" in workflow_config, "Workflow should define jobs"
    
    # Check for essential CI/CD jobs
    essential_jobs = ["security-scan", "lint", "test", "build"]
    for job in essential_jobs:
        assert job in workflow_config["jobs"], f"Workflow should have a {job} job"
    
    # Verify test job configuration
    test_job = workflow_config["jobs"]["test"]
    assert "steps" in test_job, "Test job should have steps"
    
    # Verify dependencies between jobs
    assert "needs" in workflow_config["jobs"]["test"], "Test job should depend on security and lint jobs"
    
    # Check for deploy jobs
    deploy_jobs = [job for job in workflow_config["jobs"].keys() if job.startswith("deploy")]
    assert len(deploy_jobs) > 0, "Workflow should have at least one deployment job"


def test_terraform_configuration() -> None:
    """
    Test Terraform configuration files if they exist.
    """
    terraform_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "terraform"
    )
    
    if not os.path.exists(terraform_dir):
        pytest.skip("Terraform directory does not exist")
    
    # Check for main Terraform file
    main_tf_path = os.path.join(terraform_dir, "main.tf")
    assert os.path.exists(main_tf_path), "main.tf should exist in terraform directory"
    
    # Check for variables file
    variables_tf_path = os.path.join(terraform_dir, "variables.tf")
    if os.path.exists(variables_tf_path):
        with open(variables_tf_path, "r") as f:
            content = f.read()
        assert "variable" in content, "variables.tf should define variables"