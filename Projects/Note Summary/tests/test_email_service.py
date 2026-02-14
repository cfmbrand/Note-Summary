"""Tests for the email service module."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from src.services.email_service import Email, EmailService
from src.utils.config import EmailConfig


@pytest.fixture
def email_config():
    """Return a default email configuration."""
    return EmailConfig(
        subject_pattern="[Note]",
        lookback_hours=24,
        mark_as_read=True,
    )


@pytest.fixture
def email_service(email_config):
    """Return an EmailService with a fake token."""
    return EmailService(access_token="fake-token", config=email_config)


@pytest.fixture
def sample_graph_email():
    """Return a sample Graph API email response."""
    return {
        "id": "msg-001",
        "subject": "[Note] Test note",
        "body": {"content": "<p>Hello</p>", "contentType": "html"},
        "receivedDateTime": "2026-02-14T10:00:00Z",
        "from": {"emailAddress": {"address": "user@example.com"}},
        "isRead": False,
    }


class TestEmailFromGraphResponse:
    """Tests for Email.from_graph_response."""

    def test_parses_all_fields(self, sample_graph_email):
        email = Email.from_graph_response(sample_graph_email)
        assert email.id == "msg-001"
        assert email.subject == "[Note] Test note"
        assert email.body_content == "<p>Hello</p>"
        assert email.body_content_type == "html"
        assert email.sender_email == "user@example.com"
        assert email.is_read is False

    def test_parses_datetime(self, sample_graph_email):
        email = Email.from_graph_response(sample_graph_email)
        assert email.received_datetime == datetime(2026, 2, 14, 10, 0, 0, tzinfo=timezone.utc)

    def test_missing_fields_use_defaults(self):
        minimal = {
            "id": "msg-002",
            "receivedDateTime": "2026-01-01T00:00:00Z",
        }
        email = Email.from_graph_response(minimal)
        assert email.subject == ""
        assert email.body_content == ""
        assert email.sender_email == ""
        assert email.is_read is False


class TestFetchNoteEmails:
    """Tests for EmailService.fetch_note_emails."""

    @patch("src.services.email_service.requests.get")
    def test_fetches_from_inbox_folder(self, mock_get, email_service, sample_graph_email):
        """Verify we query the Inbox folder, not all messages."""
        mock_me_response = MagicMock()
        mock_me_response.status_code = 200
        mock_me_response.json.return_value = {"mail": "user@example.com"}

        mock_messages_response = MagicMock()
        mock_messages_response.status_code = 200
        mock_messages_response.json.return_value = {"value": [sample_graph_email]}

        mock_get.side_effect = [mock_me_response, mock_messages_response]

        email_service.fetch_note_emails()

        messages_call = mock_get.call_args_list[1]
        assert "mailFolders/Inbox/messages" in messages_call.args[0]

    @patch("src.services.email_service.requests.get")
    def test_does_not_fetch_from_all_messages(self, mock_get, email_service, sample_graph_email):
        """Verify we don't use /me/messages which includes Sent Items."""
        mock_me_response = MagicMock()
        mock_me_response.status_code = 200
        mock_me_response.json.return_value = {"mail": "user@example.com"}

        mock_messages_response = MagicMock()
        mock_messages_response.status_code = 200
        mock_messages_response.json.return_value = {"value": [sample_graph_email]}

        mock_get.side_effect = [mock_me_response, mock_messages_response]

        email_service.fetch_note_emails()

        messages_call = mock_get.call_args_list[1]
        url = messages_call.args[0]
        # Should not be /me/messages (without mailFolders)
        assert "/me/messages" not in url.replace("/me/mailFolders/Inbox/messages", "")

    @patch("src.services.email_service.requests.get")
    def test_returns_parsed_emails(self, mock_get, email_service, sample_graph_email):
        mock_me_response = MagicMock()
        mock_me_response.status_code = 200
        mock_me_response.json.return_value = {"mail": "user@example.com"}

        mock_messages_response = MagicMock()
        mock_messages_response.status_code = 200
        mock_messages_response.json.return_value = {"value": [sample_graph_email]}

        mock_get.side_effect = [mock_me_response, mock_messages_response]

        emails = email_service.fetch_note_emails()
        assert len(emails) == 1
        assert emails[0].subject == "[Note] Test note"

    @patch("src.services.email_service.requests.get")
    def test_empty_inbox_returns_empty_list(self, mock_get, email_service):
        mock_me_response = MagicMock()
        mock_me_response.status_code = 200
        mock_me_response.json.return_value = {"mail": "user@example.com"}

        mock_messages_response = MagicMock()
        mock_messages_response.status_code = 200
        mock_messages_response.json.return_value = {"value": []}

        mock_get.side_effect = [mock_me_response, mock_messages_response]

        emails = email_service.fetch_note_emails()
        assert emails == []

    @patch("src.services.email_service.requests.get")
    def test_api_error_raises_runtime_error(self, mock_get, email_service):
        mock_me_response = MagicMock()
        mock_me_response.status_code = 200
        mock_me_response.json.return_value = {"mail": "user@example.com"}

        mock_messages_response = MagicMock()
        mock_messages_response.status_code = 401
        mock_messages_response.text = "Unauthorized"

        mock_get.side_effect = [mock_me_response, mock_messages_response]

        with pytest.raises(RuntimeError, match="Failed to fetch emails"):
            email_service.fetch_note_emails()


class TestMarkAsRead:
    """Tests for EmailService.mark_as_read."""

    @patch("src.services.email_service.requests.patch")
    def test_marks_email_as_read(self, mock_patch, email_service):
        mock_patch.return_value = MagicMock(status_code=200)

        result = email_service.mark_as_read("msg-001")
        assert result is True
        mock_patch.assert_called_once()
        assert mock_patch.call_args.kwargs["json"] == {"isRead": True}

    @patch("src.services.email_service.requests.patch")
    def test_returns_false_on_failure(self, mock_patch, email_service):
        mock_patch.return_value = MagicMock(status_code=500)

        result = email_service.mark_as_read("msg-001")
        assert result is False
