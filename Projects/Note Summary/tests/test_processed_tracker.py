"""Tests for SQLite-based processed email tracker."""

from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.storage.processed_tracker import ProcessedTracker


@pytest.fixture
def tracker(temp_dir: Path) -> ProcessedTracker:
    """Create a ProcessedTracker with a temp database."""
    db_path = temp_dir / "test_processed.db"
    return ProcessedTracker(db_path=db_path)


class TestProcessedTrackerInit:
    """Tests for ProcessedTracker initialization."""

    def test_creates_database_file(self, temp_dir: Path):
        """Test that initialization creates the database file."""
        db_path = temp_dir / "new_db.db"
        assert not db_path.exists()

        ProcessedTracker(db_path=db_path)

        assert db_path.exists()

    def test_creates_parent_directories(self, temp_dir: Path):
        """Test that initialization creates parent directories."""
        db_path = temp_dir / "subdir" / "nested" / "db.db"
        assert not db_path.parent.exists()

        ProcessedTracker(db_path=db_path)

        assert db_path.exists()

    def test_creates_processed_emails_table(self, temp_dir: Path):
        """Test that the processed_emails table is created."""
        import sqlite3

        db_path = temp_dir / "test.db"
        ProcessedTracker(db_path=db_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='processed_emails'"
        )
        result = cursor.fetchone()
        conn.close()

        assert result is not None
        assert result[0] == "processed_emails"

    def test_creates_tasks_table(self, temp_dir: Path):
        """Test that the tasks table is created for future extension."""
        import sqlite3

        db_path = temp_dir / "test.db"
        ProcessedTracker(db_path=db_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'"
        )
        result = cursor.fetchone()
        conn.close()

        assert result is not None


class TestMarkProcessed:
    """Tests for ProcessedTracker.mark_processed() method."""

    def test_mark_email_as_processed(self, tracker: ProcessedTracker):
        """Test marking an email as processed."""
        email_id = "test-email-1"
        received = datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

        tracker.mark_processed(
            email_id=email_id,
            subject="[Note] Test",
            received_at=received,
        )

        assert tracker.is_processed(email_id)

    def test_mark_with_onenote_page_id(self, tracker: ProcessedTracker):
        """Test marking email with OneNote page ID."""
        email_id = "test-email-2"
        page_id = "onenote-page-123"
        received = datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

        tracker.mark_processed(
            email_id=email_id,
            subject="[Note] Test",
            received_at=received,
            onenote_page_id=page_id,
        )

        # Verify via get_recent_processed
        recent = tracker.get_recent_processed(limit=1)
        assert len(recent) == 1
        assert recent[0]["onenote_page_id"] == page_id

    def test_duplicate_marking_updates_record(self, tracker: ProcessedTracker):
        """Test that marking same email twice updates the record (upsert)."""
        email_id = "test-email-3"
        received = datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

        # First mark
        tracker.mark_processed(
            email_id=email_id,
            subject="[Note] Original",
            received_at=received,
        )

        # Second mark with different subject (upsert)
        tracker.mark_processed(
            email_id=email_id,
            subject="[Note] Updated",
            received_at=received,
        )

        # Should still only be one record
        assert tracker.get_processed_count() == 1

        # Should have updated subject
        recent = tracker.get_recent_processed(limit=1)
        assert recent[0]["subject"] == "[Note] Updated"


class TestIsProcessed:
    """Tests for ProcessedTracker.is_processed() method."""

    def test_unprocessed_email_returns_false(self, tracker: ProcessedTracker):
        """Test that unprocessed email returns False."""
        assert tracker.is_processed("nonexistent-email") is False

    def test_processed_email_returns_true(self, tracker: ProcessedTracker):
        """Test that processed email returns True."""
        email_id = "processed-email"
        tracker.mark_processed(
            email_id=email_id,
            subject="[Note] Test",
            received_at=datetime.now(timezone.utc),
        )

        assert tracker.is_processed(email_id) is True

    def test_different_email_ids_tracked_separately(self, tracker: ProcessedTracker):
        """Test that different email IDs are tracked independently."""
        tracker.mark_processed(
            email_id="email-1",
            subject="[Note] First",
            received_at=datetime.now(timezone.utc),
        )

        assert tracker.is_processed("email-1") is True
        assert tracker.is_processed("email-2") is False


class TestGetProcessedCount:
    """Tests for ProcessedTracker.get_processed_count() method."""

    def test_empty_database_returns_zero(self, tracker: ProcessedTracker):
        """Test that empty database returns count of 0."""
        assert tracker.get_processed_count() == 0

    def test_count_reflects_processed_emails(self, tracker: ProcessedTracker):
        """Test that count reflects number of processed emails."""
        received = datetime.now(timezone.utc)

        for i in range(5):
            tracker.mark_processed(
                email_id=f"email-{i}",
                subject=f"[Note] Test {i}",
                received_at=received,
            )

        assert tracker.get_processed_count() == 5


class TestGetRecentProcessed:
    """Tests for ProcessedTracker.get_recent_processed() method."""

    def test_empty_database_returns_empty_list(self, tracker: ProcessedTracker):
        """Test that empty database returns empty list."""
        assert tracker.get_recent_processed() == []

    def test_returns_recent_in_descending_order(self, tracker: ProcessedTracker):
        """Test that results are ordered by processed_at descending."""
        import time

        received = datetime.now(timezone.utc)

        for i in range(3):
            tracker.mark_processed(
                email_id=f"email-{i}",
                subject=f"[Note] Test {i}",
                received_at=received,
            )
            time.sleep(0.01)  # Small delay to ensure different timestamps

        recent = tracker.get_recent_processed(limit=3)

        # Most recent should be last one added (email-2)
        assert recent[0]["email_id"] == "email-2"
        assert recent[-1]["email_id"] == "email-0"

    def test_respects_limit_parameter(self, tracker: ProcessedTracker):
        """Test that limit parameter restricts results."""
        received = datetime.now(timezone.utc)

        for i in range(10):
            tracker.mark_processed(
                email_id=f"email-{i}",
                subject=f"[Note] Test {i}",
                received_at=received,
            )

        recent = tracker.get_recent_processed(limit=5)
        assert len(recent) == 5

    def test_returns_all_fields(self, tracker: ProcessedTracker):
        """Test that returned records contain all expected fields."""
        received = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)

        tracker.mark_processed(
            email_id="test-email",
            subject="[Note] Test Subject",
            received_at=received,
            onenote_page_id="page-123",
        )

        recent = tracker.get_recent_processed(limit=1)
        record = recent[0]

        assert "email_id" in record
        assert "subject" in record
        assert "onenote_page_id" in record
        assert "processed_at" in record
        assert "received_at" in record

        assert record["email_id"] == "test-email"
        assert record["subject"] == "[Note] Test Subject"
        assert record["onenote_page_id"] == "page-123"
