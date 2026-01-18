"""Configuration management for Note Summary."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class AzureConfig:
    """Azure AD configuration."""

    client_id: str
    tenant_id: str


@dataclass
class EmailConfig:
    """Email processing configuration."""

    subject_pattern: str = "[Note]"
    lookback_hours: int = 24
    mark_as_read: bool = True


@dataclass
class OneNoteConfig:
    """OneNote configuration."""

    notebook_name: str = "Email Notes"
    section_name: str = "Captured Notes"


@dataclass
class Config:
    """Main configuration container."""

    azure: AzureConfig
    email: EmailConfig
    onenote: OneNoteConfig

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from YAML file.

        Args:
            config_path: Path to config file. If None, searches default locations.

        Returns:
            Loaded configuration.

        Raises:
            FileNotFoundError: If no config file found.
            ValueError: If config is invalid.
        """
        if config_path is None:
            config_path = cls._find_config_file()

        with open(config_path, "r") as f:
            data = yaml.safe_load(f)

        return cls._parse_config(data)

    @classmethod
    def _find_config_file(cls) -> Path:
        """Find configuration file in default locations."""
        # Check environment variable first
        env_path = os.environ.get("NOTE_SUMMARY_CONFIG")
        if env_path:
            path = Path(env_path)
            if path.exists():
                return path

        # Check relative to project root
        project_root = Path(__file__).parent.parent.parent
        candidates = [
            project_root / "config" / "config.yaml",
            project_root / "config.yaml",
            Path.home() / ".config" / "note-summary" / "config.yaml",
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        raise FileNotFoundError(
            "No config file found. Create config/config.yaml from config.example.yaml"
        )

    @classmethod
    def _parse_config(cls, data: dict) -> "Config":
        """Parse configuration dictionary."""
        if not data:
            raise ValueError("Configuration is empty")

        # Azure config is required
        azure_data = data.get("azure", {})
        if not azure_data.get("client_id"):
            raise ValueError("azure.client_id is required")
        if not azure_data.get("tenant_id"):
            raise ValueError("azure.tenant_id is required")

        azure = AzureConfig(
            client_id=azure_data["client_id"],
            tenant_id=azure_data["tenant_id"],
        )

        # Email config with defaults
        email_data = data.get("email", {})
        email = EmailConfig(
            subject_pattern=email_data.get("subject_pattern", "[Note]"),
            lookback_hours=email_data.get("lookback_hours", 24),
            mark_as_read=email_data.get("mark_as_read", True),
        )

        # OneNote config with defaults
        onenote_data = data.get("onenote", {})
        onenote = OneNoteConfig(
            notebook_name=onenote_data.get("notebook_name", "Email Notes"),
            section_name=onenote_data.get("section_name", "Captured Notes"),
        )

        return cls(azure=azure, email=email, onenote=onenote)


def get_data_dir() -> Path:
    """Get the data directory for storing tokens and database."""
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir
