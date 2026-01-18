"""Token cache management for MSAL authentication."""

import json
import os
from pathlib import Path
from typing import Optional

from msal import SerializableTokenCache

from src.utils.config import get_data_dir


class TokenCache:
    """Persistent token cache for MSAL."""

    def __init__(self, cache_file: Optional[Path] = None):
        """Initialize token cache.

        Args:
            cache_file: Path to cache file. Defaults to data/token_cache.json.
        """
        if cache_file is None:
            cache_file = get_data_dir() / "token_cache.json"

        self._cache_file = cache_file
        self._cache = SerializableTokenCache()
        self._load()

    @property
    def cache(self) -> SerializableTokenCache:
        """Get the MSAL serializable token cache."""
        return self._cache

    def _load(self) -> None:
        """Load cache from disk if it exists."""
        if self._cache_file.exists():
            try:
                with open(self._cache_file, "r") as f:
                    self._cache.deserialize(f.read())
            except (json.JSONDecodeError, OSError):
                # Cache file corrupted or unreadable, start fresh
                pass

    def save(self) -> None:
        """Save cache to disk if it has changed."""
        if self._cache.has_state_changed:
            # Ensure parent directory exists
            self._cache_file.parent.mkdir(parents=True, exist_ok=True)

            # Write with restricted permissions (user read/write only)
            with open(self._cache_file, "w") as f:
                f.write(self._cache.serialize())

            # Set file permissions to 600 (owner read/write only)
            os.chmod(self._cache_file, 0o600)

    def clear(self) -> None:
        """Clear the token cache."""
        self._cache = SerializableTokenCache()
        if self._cache_file.exists():
            self._cache_file.unlink()
