"""Shared pytest fixtures for Note Summary tests."""

import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def valid_config_data() -> dict:
    """Return valid configuration data."""
    return {
        "azure": {
            "client_id": "test-client-id",
            "tenant_id": "test-tenant-id",
        },
        "email": {
            "subject_pattern": "[Note]",
            "lookback_hours": 24,
            "mark_as_read": True,
        },
        "onenote": {
            "notebook_name": "Test Notebook",
            "section_name": "Test Section",
        },
    }


@pytest.fixture
def minimal_config_data() -> dict:
    """Return minimal valid configuration (only required fields)."""
    return {
        "azure": {
            "client_id": "test-client-id",
            "tenant_id": "test-tenant-id",
        }
    }


@pytest.fixture
def sample_email_data() -> dict:
    """Return sample email data for testing."""
    return {
        "id": "test-email-id-123",
        "subject": "[Note] Test Note Title",
        "body_content": "This is the email body content.",
        "body_content_type": "text",
        "received_datetime": datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
        "sender_email": "test@example.com",
        "is_read": False,
    }


@pytest.fixture
def config_file(temp_dir: Path, valid_config_data: dict) -> Path:
    """Create a temporary config file with valid configuration."""
    import yaml

    config_path = temp_dir / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(valid_config_data, f)
    return config_path


@pytest.fixture
def empty_config_file(temp_dir: Path) -> Path:
    """Create a temporary empty config file."""
    config_path = temp_dir / "config.yaml"
    with open(config_path, "w") as f:
        f.write("")
    return config_path
