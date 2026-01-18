"""Email service for fetching emails from Outlook via Microsoft Graph API."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import requests

from src.utils.config import EmailConfig


GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


@dataclass
class Email:
    """Represents an email message."""

    id: str
    subject: str
    body_content: str
    body_content_type: str
    received_datetime: datetime
    sender_email: str
    is_read: bool

    @classmethod
    def from_graph_response(cls, data: dict) -> "Email":
        """Create Email from Graph API response."""
        return cls(
            id=data["id"],
            subject=data.get("subject", ""),
            body_content=data.get("body", {}).get("content", ""),
            body_content_type=data.get("body", {}).get("contentType", "text"),
            received_datetime=datetime.fromisoformat(
                data["receivedDateTime"].replace("Z", "+00:00")
            ),
            sender_email=data.get("from", {}).get("emailAddress", {}).get("address", ""),
            is_read=data.get("isRead", False),
        )


class EmailService:
    """Service for interacting with Outlook emails via Graph API."""

    def __init__(self, access_token: str, config: EmailConfig):
        """Initialize email service.

        Args:
            access_token: Microsoft Graph API access token.
            config: Email configuration.
        """
        self._access_token = access_token
        self._config = config
        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        self._user_email: Optional[str] = None

    def get_current_user_email(self) -> str:
        """Get the current user's email address.

        Returns:
            User's email address.

        Raises:
            RuntimeError: If API call fails.
        """
        if self._user_email:
            return self._user_email

        response = requests.get(f"{GRAPH_BASE_URL}/me", headers=self._headers)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to get user info: {response.text}")

        data = response.json()
        self._user_email = data.get("mail") or data.get("userPrincipalName", "")
        return self._user_email

    def fetch_note_emails(self) -> List[Email]:
        """Fetch emails matching the note subject pattern.

        Returns self-sent emails from the configured lookback period
        that start with the configured subject pattern.

        Returns:
            List of matching emails.

        Raises:
            RuntimeError: If API call fails.
        """
        user_email = self.get_current_user_email()
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=self._config.lookback_hours)
        cutoff_str = cutoff_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Build OData filter for self-sent emails with matching subject
        # Note: startsWith is case-insensitive in Graph API
        filter_query = (
            f"receivedDateTime ge {cutoff_str} "
            f"and startsWith(subject, '{self._config.subject_pattern}') "
            f"and from/emailAddress/address eq '{user_email}'"
        )

        params = {
            "$filter": filter_query,
            "$select": "id,subject,body,receivedDateTime,from,isRead",
            "$orderby": "receivedDateTime desc",
            "$top": 50,
        }

        response = requests.get(
            f"{GRAPH_BASE_URL}/me/messages",
            headers=self._headers,
            params=params,
        )

        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch emails: {response.text}")

        data = response.json()
        emails = [Email.from_graph_response(msg) for msg in data.get("value", [])]

        return emails

    def mark_as_read(self, email_id: str) -> bool:
        """Mark an email as read.

        Args:
            email_id: The email message ID.

        Returns:
            True if successful.
        """
        if not self._config.mark_as_read:
            return True

        response = requests.patch(
            f"{GRAPH_BASE_URL}/me/messages/{email_id}",
            headers=self._headers,
            json={"isRead": True},
        )

        return response.status_code == 200
