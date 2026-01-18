"""Tests for email to OneNote note processor."""

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from src.processors.email_processor import EmailProcessor, ProcessedNote
from src.services.email_service import Email
from src.utils.config import EmailConfig


@pytest.fixture
def email_config() -> EmailConfig:
    """Create default email config for testing."""
    return EmailConfig(
        subject_pattern="[Note]",
        lookback_hours=24,
        mark_as_read=True,
    )


@pytest.fixture
def processor(email_config: EmailConfig) -> EmailProcessor:
    """Create email processor for testing."""
    return EmailProcessor(email_config)


@pytest.fixture
def sample_email() -> Email:
    """Create a sample email for testing."""
    return Email(
        id="test-email-123",
        subject="[Note] Test Note Title",
        body_content="This is the body content.",
        body_content_type="text",
        received_datetime=datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
        sender_email="test@example.com",
        is_read=False,
    )


class TestExtractTitle:
    """Tests for EmailProcessor.extract_title() method."""

    def test_extract_title_standard(self, processor: EmailProcessor):
        """Test extracting title from standard [Note] prefix."""
        title = processor.extract_title("[Note] My Title")
        assert title == "My Title"

    def test_extract_title_case_insensitive(self, processor: EmailProcessor):
        """Test extracting title is case-insensitive."""
        assert processor.extract_title("[note] Lowercase Prefix") == "Lowercase Prefix"
        assert processor.extract_title("[NOTE] Uppercase Prefix") == "Uppercase Prefix"
        assert processor.extract_title("[NoTe] Mixed Case") == "Mixed Case"

    def test_extract_title_strips_whitespace(self, processor: EmailProcessor):
        """Test that extra whitespace is stripped from title."""
        assert processor.extract_title("[Note]   Extra Spaces   ") == "Extra Spaces"
        assert processor.extract_title("[Note]\tTabbed Title") == "Tabbed Title"

    def test_extract_title_empty_returns_untitled(self, processor: EmailProcessor):
        """Test that empty title returns 'Untitled Note'."""
        assert processor.extract_title("[Note]") == "Untitled Note"
        assert processor.extract_title("[Note]   ") == "Untitled Note"

    def test_extract_title_no_prefix_returns_full_subject(self, processor: EmailProcessor):
        """Test subject without prefix returns full subject."""
        assert processor.extract_title("Regular Subject") == "Regular Subject"

    def test_extract_title_different_prefix(self):
        """Test extraction with different subject pattern."""
        config = EmailConfig(subject_pattern="[Task]")
        processor = EmailProcessor(config)

        assert processor.extract_title("[Task] Do Something") == "Do Something"
        assert processor.extract_title("[Note] Different Pattern") == "[Note] Different Pattern"


class TestCleanHtmlContent:
    """Tests for EmailProcessor.clean_html_content() method."""

    def test_plain_text_to_html(self, processor: EmailProcessor):
        """Test converting plain text to HTML."""
        text = "Line 1\nLine 2\nLine 3"
        result = processor.clean_html_content(text, "text")

        assert "<br>" in result
        assert "Line 1" in result
        assert "Line 2" in result
        assert "<div>" in result

    def test_plain_text_escapes_html_entities(self, processor: EmailProcessor):
        """Test that special characters are escaped in plain text."""
        text = "Use <tag> and & symbol"
        result = processor.clean_html_content(text, "text")

        assert "&lt;tag&gt;" in result
        assert "&amp;" in result

    def test_html_removes_script_tags(self, processor: EmailProcessor):
        """Test that <script> tags are removed from HTML."""
        html = "<div>Content</div><script>alert('xss')</script><p>More</p>"
        result = processor.clean_html_content(html, "html")

        assert "<script>" not in result
        assert "alert" not in result
        assert "<div>Content</div>" in result
        assert "<p>More</p>" in result

    def test_html_removes_style_tags(self, processor: EmailProcessor):
        """Test that <style> tags are removed from HTML."""
        html = "<style>.class { color: red; }</style><div>Content</div>"
        result = processor.clean_html_content(html, "html")

        assert "<style>" not in result
        assert ".class" not in result
        assert "<div>Content</div>" in result

    def test_html_removes_wrapper_tags(self, processor: EmailProcessor):
        """Test that html/head/body wrapper tags are removed."""
        html = """<!DOCTYPE html>
<html>
<head><title>Email</title></head>
<body><div>Content</div></body>
</html>"""
        result = processor.clean_html_content(html, "html")

        assert "<!DOCTYPE" not in result
        assert "<html>" not in result
        assert "</html>" not in result
        assert "<head>" not in result
        assert "</head>" not in result
        assert "<body>" not in result
        assert "</body>" not in result
        assert "<div>Content</div>" in result

    def test_html_case_insensitive_tag_removal(self, processor: EmailProcessor):
        """Test that tag removal is case-insensitive."""
        html = "<SCRIPT>code</SCRIPT><STYLE>css</STYLE><HTML><BODY>content</BODY></HTML>"
        result = processor.clean_html_content(html, "html")

        assert "<SCRIPT>" not in result
        assert "<STYLE>" not in result
        assert "<HTML>" not in result
        assert "<BODY>" not in result


class TestCreateMetadataFooter:
    """Tests for EmailProcessor.create_metadata_footer() method."""

    def test_footer_contains_received_date(self, processor: EmailProcessor, sample_email: Email):
        """Test that footer contains the received date."""
        footer = processor.create_metadata_footer(sample_email)

        assert "2024-01-15 10:30:00 UTC" in footer

    def test_footer_contains_hr_separator(self, processor: EmailProcessor, sample_email: Email):
        """Test that footer contains hr separator."""
        footer = processor.create_metadata_footer(sample_email)

        assert "<hr>" in footer

    def test_footer_contains_note_captured_text(self, processor: EmailProcessor, sample_email: Email):
        """Test that footer contains explanatory text."""
        footer = processor.create_metadata_footer(sample_email)

        assert "Note captured from email" in footer


class TestProcessEmail:
    """Tests for EmailProcessor.process_email() method."""

    def test_process_email_returns_processed_note(self, processor: EmailProcessor, sample_email: Email):
        """Test that process_email returns a ProcessedNote."""
        result = processor.process_email(sample_email)

        assert isinstance(result, ProcessedNote)
        assert result.email_id == sample_email.id
        assert result.received_datetime == sample_email.received_datetime

    def test_process_email_extracts_title(self, processor: EmailProcessor, sample_email: Email):
        """Test that process_email extracts the title correctly."""
        result = processor.process_email(sample_email)

        assert result.title == "Test Note Title"

    def test_process_email_includes_body_and_footer(self, processor: EmailProcessor, sample_email: Email):
        """Test that HTML content includes body and footer."""
        result = processor.process_email(sample_email)

        assert "This is the body content." in result.html_content
        assert "<hr>" in result.html_content
        assert "Note captured from email" in result.html_content

    def test_process_html_email(self, processor: EmailProcessor):
        """Test processing an HTML email."""
        email = Email(
            id="html-email",
            subject="[Note] HTML Email",
            body_content="<p>Formatted <strong>content</strong></p>",
            body_content_type="html",
            received_datetime=datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
            sender_email="test@example.com",
            is_read=False,
        )

        result = processor.process_email(email)

        assert "<p>Formatted <strong>content</strong></p>" in result.html_content
        assert result.title == "HTML Email"
