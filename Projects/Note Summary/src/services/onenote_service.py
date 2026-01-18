"""OneNote service for creating pages via Microsoft Graph API."""

from dataclasses import dataclass
from typing import List, Optional

import requests

from src.utils.config import OneNoteConfig


GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


@dataclass
class Notebook:
    """Represents a OneNote notebook."""

    id: str
    display_name: str


@dataclass
class Section:
    """Represents a OneNote section."""

    id: str
    display_name: str
    notebook_id: str


class OneNoteService:
    """Service for interacting with OneNote via Graph API."""

    def __init__(self, access_token: str, config: OneNoteConfig):
        """Initialize OneNote service.

        Args:
            access_token: Microsoft Graph API access token.
            config: OneNote configuration.
        """
        self._access_token = access_token
        self._config = config
        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        self._cached_section_id: Optional[str] = None

    def list_notebooks(self) -> List[Notebook]:
        """List all notebooks.

        Returns:
            List of notebooks.

        Raises:
            RuntimeError: If API call fails.
        """
        response = requests.get(
            f"{GRAPH_BASE_URL}/me/onenote/notebooks",
            headers=self._headers,
        )

        if response.status_code != 200:
            raise RuntimeError(f"Failed to list notebooks: {response.text}")

        data = response.json()
        return [
            Notebook(id=nb["id"], display_name=nb["displayName"])
            for nb in data.get("value", [])
        ]

    def list_sections(self, notebook_id: str) -> List[Section]:
        """List all sections in a notebook.

        Args:
            notebook_id: The notebook ID.

        Returns:
            List of sections.

        Raises:
            RuntimeError: If API call fails.
        """
        response = requests.get(
            f"{GRAPH_BASE_URL}/me/onenote/notebooks/{notebook_id}/sections",
            headers=self._headers,
        )

        if response.status_code != 200:
            raise RuntimeError(f"Failed to list sections: {response.text}")

        data = response.json()
        return [
            Section(id=s["id"], display_name=s["displayName"], notebook_id=notebook_id)
            for s in data.get("value", [])
        ]

    def get_or_create_target_section(self) -> str:
        """Get or create the target section for notes.

        Returns:
            Section ID.

        Raises:
            RuntimeError: If unable to find or create section.
        """
        if self._cached_section_id:
            return self._cached_section_id

        # Find or create notebook
        notebook_id = self._get_or_create_notebook()

        # Find or create section
        section_id = self._get_or_create_section(notebook_id)

        self._cached_section_id = section_id
        return section_id

    def _get_or_create_notebook(self) -> str:
        """Get or create the target notebook.

        Returns:
            Notebook ID.
        """
        notebooks = self.list_notebooks()

        # Look for existing notebook
        for nb in notebooks:
            if nb.display_name.lower() == self._config.notebook_name.lower():
                return nb.id

        # Create new notebook
        response = requests.post(
            f"{GRAPH_BASE_URL}/me/onenote/notebooks",
            headers=self._headers,
            json={"displayName": self._config.notebook_name},
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Failed to create notebook: {response.text}")

        return response.json()["id"]

    def _get_or_create_section(self, notebook_id: str) -> str:
        """Get or create the target section.

        Args:
            notebook_id: The notebook ID.

        Returns:
            Section ID.
        """
        sections = self.list_sections(notebook_id)

        # Look for existing section
        for section in sections:
            if section.display_name.lower() == self._config.section_name.lower():
                return section.id

        # Create new section
        response = requests.post(
            f"{GRAPH_BASE_URL}/me/onenote/notebooks/{notebook_id}/sections",
            headers=self._headers,
            json={"displayName": self._config.section_name},
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Failed to create section: {response.text}")

        return response.json()["id"]

    def create_page(self, title: str, html_content: str) -> str:
        """Create a new page in the target section.

        Args:
            title: Page title.
            html_content: HTML content for the page body.

        Returns:
            The created page ID.

        Raises:
            RuntimeError: If page creation fails.
        """
        section_id = self.get_or_create_target_section()

        # OneNote API requires specific HTML structure
        page_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    {html_content}
</body>
</html>"""

        # OneNote pages endpoint requires text/html content type
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "text/html",
        }

        response = requests.post(
            f"{GRAPH_BASE_URL}/me/onenote/sections/{section_id}/pages",
            headers=headers,
            data=page_html.encode("utf-8"),
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Failed to create page: {response.text}")

        return response.json()["id"]
