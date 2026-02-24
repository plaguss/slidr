"""Serve deck with file watching and auto-rebuild."""

import argparse
import os
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from typing import Any

from watchfiles import watch

from .build import build_deck
from .logging_utils import get_logger

logger = get_logger(__name__)


class QuietRequestHandler(SimpleHTTPRequestHandler):
    """HTTP handler that suppresses access logs."""

    def log_message(self, format: str, *args: Any) -> None:
        return  # pragma: no cover


def create_build_args(deck_dir: Path, theme: str | None) -> argparse.Namespace:
    """
    Create build arguments namespace.

    Args:
        deck_dir: Path to the deck directory
        theme: Optional path to custom CSS theme

    Returns:
        Namespace object with build arguments
    """
    return argparse.Namespace(
        deck=str(deck_dir),
        output=str(deck_dir / "index.html"),
        theme=theme,
        live_reload=True,
    )


def serve_deck(args: argparse.Namespace) -> int:
    """
    Serve deck with file watching and auto-rebuild.

    Args:
        args: Parsed command-line arguments containing:
            - deck: Path to the deck folder
            - port: Port to serve on
            - theme: Optional path to custom CSS theme

    Returns:
        Exit code (0 for success)

    Raises:
        FileNotFoundError: If deck directory not found
    """
    deck_dir = Path(args.deck).resolve()

    if not deck_dir.exists():
        raise FileNotFoundError(f"Deck directory not found: {deck_dir}")

    logger.info(f"🚀 Starting server on http://localhost:{args.port}")
    logger.info(f"📁 Serving from {deck_dir}")
    logger.info("Watching for changes...")
    logger.info("Press Ctrl+C to stop.\n")

    # Initial build
    build_args = create_build_args(deck_dir, args.theme)
    build_deck(build_args)

    # Start server in background
    os.chdir(deck_dir)

    server = HTTPServer(("localhost", args.port), QuietRequestHandler)
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Watch for changes
    def rebuild_on_changes() -> None:
        """Watch for file changes and rebuild when detected."""
        last_build = time.time()
        for _ in watch(str(deck_dir), watch_filter=lambda *_: True):
            current_time = time.time()
            # Debounce: only rebuild if at least 1 second has passed
            if current_time - last_build >= 1:
                logger.info("🔄 Changes detected, rebuilding...")
                try:
                    build_args = create_build_args(deck_dir, args.theme)
                    build_deck(build_args)
                    last_build = current_time
                except Exception as e:
                    logger.error(f"❌ Build failed: {e}")

    try:
        rebuild_on_changes()
    except KeyboardInterrupt:
        logger.info("✓ Server stopped")
        server.shutdown()

    return 0
