#!/usr/bin/env python3
"""Note Summary - Monitor Outlook for self-sent notes and create OneNote pages."""

import argparse
import logging
import sys
import time
from pathlib import Path

from src.auth.graph_auth import GraphAuth
from src.processors.email_processor import EmailProcessor
from src.services.email_service import EmailService
from src.services.onenote_service import OneNoteService
from src.storage.processed_tracker import ProcessedTracker
from src.utils.config import Config


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool) -> None:
    """Configure logging level."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")


def authenticate(config: Config, auth_only: bool = False) -> str:
    """Authenticate and get access token.

    Args:
        config: Application configuration.
        auth_only: If True, just authenticate and exit.

    Returns:
        Access token.
    """
    auth = GraphAuth(config.azure)

    if auth_only:
        logger.info("Running authentication only...")
        token = auth.get_access_token(interactive=True)
        if token:
            logger.info("Authentication successful! Token cached for future use.")
            sys.exit(0)
        else:
            logger.error("Authentication failed.")
            sys.exit(1)

    # Try silent auth first, then interactive
    token = auth.get_access_token(interactive=False)
    if not token:
        logger.info("No cached credentials. Starting interactive authentication...")
        token = auth.get_access_token(interactive=True)

    if not token:
        logger.error("Failed to authenticate. Run with --auth-only to authenticate.")
        sys.exit(1)

    return token


def list_notebooks(config: Config, token: str) -> None:
    """List available notebooks and sections."""
    onenote = OneNoteService(token, config.onenote)

    print("\nAvailable OneNote Notebooks:")
    print("=" * 50)

    try:
        notebooks = onenote.list_notebooks()
        if not notebooks:
            print("No notebooks found.")
            return

        for nb in notebooks:
            print(f"\n  Notebook: {nb.display_name}")
            print(f"  ID: {nb.id}")

            sections = onenote.list_sections(nb.id)
            if sections:
                print("  Sections:")
                for section in sections:
                    print(f"    - {section.display_name}")
            else:
                print("  Sections: (none)")

    except Exception as e:
        logger.error(f"Failed to list notebooks: {e}")
        sys.exit(1)


def process_emails(config: Config, token: str, dry_run: bool = False) -> int:
    """Process pending note emails.

    Args:
        config: Application configuration.
        token: Access token.
        dry_run: If True, don't actually create notes.

    Returns:
        Number of emails processed.
    """
    email_service = EmailService(token, config.email)
    onenote_service = OneNoteService(token, config.onenote)
    processor = EmailProcessor(config.email)
    tracker = ProcessedTracker()

    logger.info(f"Fetching emails with subject pattern: {config.email.subject_pattern}")
    logger.info(f"Looking back {config.email.lookback_hours} hours")

    try:
        emails = email_service.fetch_note_emails()
    except Exception as e:
        logger.error(f"Failed to fetch emails: {e}")
        return 0

    if not emails:
        logger.info("No matching emails found.")
        return 0

    logger.info(f"Found {len(emails)} matching email(s)")

    processed_count = 0
    for email in emails:
        # Skip already processed emails
        if tracker.is_processed(email.id):
            logger.debug(f"Skipping already processed: {email.subject}")
            continue

        logger.info(f"Processing: {email.subject}")

        try:
            # Process email into note format
            note = processor.process_email(email)

            if dry_run:
                logger.info(f"  [DRY RUN] Would create note: {note.title}")
                continue

            # Create OneNote page
            page_id = onenote_service.create_page(note.title, note.html_content)
            logger.info(f"  Created OneNote page: {note.title}")

            # Mark as processed
            tracker.mark_processed(
                email_id=email.id,
                subject=email.subject,
                received_at=email.received_datetime,
                onenote_page_id=page_id,
            )

            # Optionally mark email as read
            if config.email.mark_as_read and not email.is_read:
                email_service.mark_as_read(email.id)
                logger.debug(f"  Marked email as read")

            processed_count += 1

        except Exception as e:
            logger.error(f"  Failed to process email: {e}")
            continue

    logger.info(f"Processed {processed_count} new email(s)")
    return processed_count


def run_daemon(config: Config, token: str, interval: int = 300) -> None:
    """Run in continuous monitoring mode.

    Args:
        config: Application configuration.
        token: Access token.
        interval: Seconds between checks.
    """
    logger.info(f"Starting daemon mode. Checking every {interval} seconds.")
    logger.info("Press Ctrl+C to stop.")

    auth = GraphAuth(config.azure)

    while True:
        try:
            # Refresh token if needed
            current_token = auth.get_access_token(interactive=False)
            if not current_token:
                logger.warning("Token expired. Please re-authenticate.")
                break

            process_emails(config, current_token)

        except KeyboardInterrupt:
            logger.info("Shutting down...")
            break
        except Exception as e:
            logger.error(f"Error during processing: {e}")

        time.sleep(interval)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Monitor Outlook for self-sent notes and create OneNote pages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main --auth-only       # Initial authentication
  python -m src.main --list-notebooks  # Show available notebooks
  python -m src.main                   # Process pending emails
  python -m src.main --daemon          # Continuous monitoring
        """,
    )

    parser.add_argument(
        "--auth-only",
        action="store_true",
        help="Only perform authentication (for initial setup)",
    )
    parser.add_argument(
        "--list-notebooks",
        action="store_true",
        help="List available OneNote notebooks and sections",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run in continuous monitoring mode",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Seconds between checks in daemon mode (default: 300)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without making changes",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file",
    )

    args = parser.parse_args()

    # Set up logging
    setup_logging(args.verbose)

    # Load configuration
    try:
        config = Config.load(args.config)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    # Authenticate
    token = authenticate(config, auth_only=args.auth_only)

    # Execute requested action
    if args.list_notebooks:
        list_notebooks(config, token)
    elif args.daemon:
        run_daemon(config, token, args.interval)
    else:
        processed = process_emails(config, token, dry_run=args.dry_run)
        if args.dry_run:
            logger.info("Dry run complete. No changes made.")


if __name__ == "__main__":
    main()
