"""Email to OneNote note processor."""

import html
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.services.email_service import Email
from src.utils.config import EmailConfig


@dataclass
class ProcessedNote:
    """Represents a note ready for OneNote."""

    email_id: str
    title: str
    html_content: str
    received_datetime: datetime


class EmailProcessor:
    """Process emails into OneNote-compatible notes."""

    def __init__(self, config: EmailConfig):
        """Initialize email processor.

        Args:
            config: Email configuration.
        """
        self._config = config
        self._pattern = config.subject_pattern

    def extract_title(self, subject: str) -> str:
        """Extract note title from email subject.

        Removes the subject pattern prefix and strips whitespace.

        Args:
            subject: Email subject line.

        Returns:
            Extracted title.
        """
        # Remove the pattern prefix (case-insensitive)
        pattern_len = len(self._pattern)
        if subject.lower().startswith(self._pattern.lower()):
            title = subject[pattern_len:].strip()
        else:
            title = subject.strip()

        # Ensure we have a title
        return title if title else "Untitled Note"

    def clean_html_content(self, content: str, content_type: str) -> str:
        """Clean and prepare HTML content for OneNote.

        Args:
            content: Email body content.
            content_type: Content type (html or text).

        Returns:
            Cleaned HTML suitable for OneNote.
        """
        if content_type.lower() == "text":
            # Convert plain text to HTML
            escaped = html.escape(content)
            # Convert newlines to <br> tags
            html_content = escaped.replace("\n", "<br>\n")
            return f"<div>{html_content}</div>"

        # For HTML content, do minimal cleaning
        cleaned = content

        # Remove potentially problematic elements
        # Remove <script> tags
        cleaned = re.sub(r"<script[^>]*>.*?</script>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
        # Remove <style> tags
        cleaned = re.sub(r"<style[^>]*>.*?</style>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML/HEAD/BODY wrapper tags (OneNote will add its own)
        cleaned = re.sub(r"</?html[^>]*>", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<head[^>]*>.*?</head>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r"</?body[^>]*>", "", cleaned, flags=re.IGNORECASE)
        # Remove DOCTYPE declarations
        cleaned = re.sub(r"<!DOCTYPE[^>]*>", "", cleaned, flags=re.IGNORECASE)

        return cleaned.strip()

    def create_metadata_footer(self, email: Email) -> str:
        """Create a metadata footer for the note.

        Args:
            email: Source email.

        Returns:
            HTML metadata footer.
        """
        received_str = email.received_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

        return f"""
<hr>
<div style="color: #666; font-size: 0.9em;">
    <p><strong>Note captured from email</strong></p>
    <p>Received: {received_str}</p>
</div>
"""

    def process_email(self, email: Email) -> ProcessedNote:
        """Process an email into a note.

        Args:
            email: Email to process.

        Returns:
            Processed note ready for OneNote.
        """
        title = self.extract_title(email.subject)
        body_html = self.clean_html_content(email.body_content, email.body_content_type)
        footer = self.create_metadata_footer(email)

        html_content = f"{body_html}\n{footer}"

        return ProcessedNote(
            email_id=email.id,
            title=title,
            html_content=html_content,
            received_datetime=email.received_datetime,
        )
