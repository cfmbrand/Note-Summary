"""Tests for configuration loading and validation."""

import os
from pathlib import Path

import pytest
import yaml

from src.utils.config import AzureConfig, Config, EmailConfig, OneNoteConfig


class TestConfigLoad:
    """Tests for Config.load() method."""

    def test_load_valid_config(self, config_file: Path, valid_config_data: dict):
        """Test loading a valid configuration file."""
        config = Config.load(config_file)

        assert config.azure.client_id == valid_config_data["azure"]["client_id"]
        assert config.azure.tenant_id == valid_config_data["azure"]["tenant_id"]
        assert config.email.subject_pattern == valid_config_data["email"]["subject_pattern"]
        assert config.email.lookback_hours == valid_config_data["email"]["lookback_hours"]
        assert config.email.mark_as_read == valid_config_data["email"]["mark_as_read"]
        assert config.onenote.notebook_name == valid_config_data["onenote"]["notebook_name"]
        assert config.onenote.section_name == valid_config_data["onenote"]["section_name"]

    def test_load_minimal_config_applies_defaults(self, temp_dir: Path, minimal_config_data: dict):
        """Test that defaults are applied for optional fields."""
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(minimal_config_data, f)

        config = Config.load(config_path)

        # Required fields should be present
        assert config.azure.client_id == "test-client-id"
        assert config.azure.tenant_id == "test-tenant-id"

        # Optional fields should have defaults
        assert config.email.subject_pattern == "[Note]"
        assert config.email.lookback_hours == 24
        assert config.email.mark_as_read is True
        assert config.onenote.notebook_name == "Email Notes"
        assert config.onenote.section_name == "Captured Notes"

    def test_missing_client_id_raises_error(self, temp_dir: Path):
        """Test that missing client_id raises ValueError."""
        config_data = {
            "azure": {
                "tenant_id": "test-tenant-id",
            }
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)

        with pytest.raises(ValueError, match="azure.client_id is required"):
            Config.load(config_path)

    def test_missing_tenant_id_raises_error(self, temp_dir: Path):
        """Test that missing tenant_id raises ValueError."""
        config_data = {
            "azure": {
                "client_id": "test-client-id",
            }
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)

        with pytest.raises(ValueError, match="azure.tenant_id is required"):
            Config.load(config_path)

    def test_empty_config_raises_error(self, empty_config_file: Path):
        """Test that empty config file raises ValueError."""
        with pytest.raises(ValueError, match="Configuration is empty"):
            Config.load(empty_config_file)

    def test_missing_config_file_raises_error(self, temp_dir: Path):
        """Test that missing config file raises FileNotFoundError."""
        nonexistent_path = temp_dir / "nonexistent.yaml"

        with pytest.raises(FileNotFoundError):
            Config.load(nonexistent_path)


class TestConfigFindFile:
    """Tests for Config._find_config_file() method."""

    def test_find_config_via_env_var(self, config_file: Path, monkeypatch: pytest.MonkeyPatch):
        """Test finding config via NOTE_SUMMARY_CONFIG environment variable."""
        monkeypatch.setenv("NOTE_SUMMARY_CONFIG", str(config_file))

        found_path = Config._find_config_file()
        assert found_path == config_file

    def test_env_var_file_not_found_continues_search(self, temp_dir: Path, monkeypatch: pytest.MonkeyPatch):
        """Test that search continues if env var file doesn't exist."""
        nonexistent = temp_dir / "nonexistent.yaml"
        monkeypatch.setenv("NOTE_SUMMARY_CONFIG", str(nonexistent))

        # Mock the module's __file__ to point to temp dir so no config found
        import src.utils.config as config_module

        fake_module_path = temp_dir / "src" / "utils" / "config.py"
        fake_module_path.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(config_module, "__file__", str(fake_module_path))

        # Should raise FileNotFoundError since no other config files exist
        with pytest.raises(FileNotFoundError):
            Config._find_config_file()

    def test_no_config_found_raises_error(self, monkeypatch: pytest.MonkeyPatch, temp_dir: Path):
        """Test that FileNotFoundError is raised when no config exists."""
        # Clear the environment variable
        monkeypatch.delenv("NOTE_SUMMARY_CONFIG", raising=False)

        # Mock the module's __file__ to point to temp dir so no config found
        import src.utils.config as config_module

        fake_module_path = temp_dir / "src" / "utils" / "config.py"
        fake_module_path.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(config_module, "__file__", str(fake_module_path))

        # This will search default locations and fail
        with pytest.raises(FileNotFoundError, match="No config file found"):
            Config._find_config_file()


class TestConfigParseConfig:
    """Tests for Config._parse_config() method."""

    def test_parse_full_config(self, valid_config_data: dict):
        """Test parsing a complete configuration dictionary."""
        config = Config._parse_config(valid_config_data)

        assert isinstance(config, Config)
        assert isinstance(config.azure, AzureConfig)
        assert isinstance(config.email, EmailConfig)
        assert isinstance(config.onenote, OneNoteConfig)

    def test_parse_custom_email_settings(self):
        """Test parsing custom email configuration values."""
        data = {
            "azure": {"client_id": "id", "tenant_id": "tenant"},
            "email": {
                "subject_pattern": "[Task]",
                "lookback_hours": 48,
                "mark_as_read": False,
            },
        }

        config = Config._parse_config(data)

        assert config.email.subject_pattern == "[Task]"
        assert config.email.lookback_hours == 48
        assert config.email.mark_as_read is False

    def test_parse_custom_onenote_settings(self):
        """Test parsing custom OneNote configuration values."""
        data = {
            "azure": {"client_id": "id", "tenant_id": "tenant"},
            "onenote": {
                "notebook_name": "My Notes",
                "section_name": "Emails",
            },
        }

        config = Config._parse_config(data)

        assert config.onenote.notebook_name == "My Notes"
        assert config.onenote.section_name == "Emails"

    def test_parse_none_data_raises_error(self):
        """Test that None data raises ValueError."""
        with pytest.raises(ValueError, match="Configuration is empty"):
            Config._parse_config(None)

    def test_parse_empty_dict_raises_error(self):
        """Test that empty dict raises ValueError."""
        with pytest.raises(ValueError, match="Configuration is empty"):
            Config._parse_config({})
