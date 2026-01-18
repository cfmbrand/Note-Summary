"""SQLite-based tracker for processed emails to prevent duplicates."""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, List, Optional

from src.utils.config import get_data_dir


class ProcessedTracker:
    """Track processed emails using SQLite database."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize processed tracker.

        Args:
            db_path: Path to SQLite database. Defaults to data/processed.db.
        """
        if db_path is None:
            db_path = get_data_dir() / "processed.db"

        self._db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database schema."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Table for processed emails
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processed_emails (
                    email_id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    onenote_page_id TEXT,
                    processed_at TEXT NOT NULL,
                    received_at TEXT NOT NULL
                )
            """)

            # Index for faster lookups by processed time
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_processed_at
                ON processed_emails(processed_at)
            """)

            # Future extension: tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email_id TEXT UNIQUE,
                    title TEXT NOT NULL,
                    due_date TEXT,
                    completed INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
            """)

            conn.commit()

    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get database connection context manager."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def is_processed(self, email_id: str) -> bool:
        """Check if an email has already been processed.

        Args:
            email_id: The email message ID.

        Returns:
            True if the email has been processed.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM processed_emails WHERE email_id = ?",
                (email_id,)
            )
            return cursor.fetchone() is not None

    def mark_processed(
        self,
        email_id: str,
        subject: str,
        received_at: datetime,
        onenote_page_id: Optional[str] = None,
    ) -> None:
        """Mark an email as processed.

        Args:
            email_id: The email message ID.
            subject: Email subject.
            received_at: When the email was received.
            onenote_page_id: The created OneNote page ID.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO processed_emails
                (email_id, subject, onenote_page_id, processed_at, received_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    email_id,
                    subject,
                    onenote_page_id,
                    datetime.utcnow().isoformat(),
                    received_at.isoformat(),
                ),
            )
            conn.commit()

    def get_processed_count(self) -> int:
        """Get the total number of processed emails.

        Returns:
            Count of processed emails.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM processed_emails")
            row = cursor.fetchone()
            return row[0] if row else 0

    def get_recent_processed(self, limit: int = 10) -> List[dict]:
        """Get recently processed emails.

        Args:
            limit: Maximum number of records to return.

        Returns:
            List of processed email records.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT email_id, subject, onenote_page_id, processed_at, received_at
                FROM processed_emails
                ORDER BY processed_at DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
