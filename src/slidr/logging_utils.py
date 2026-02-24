"""Logging utilities for slidr."""

import logging

from rich.console import Console
from rich.logging import RichHandler

# Create a console for rich output
console = Console(stderr=False, force_terminal=True)


def configure_logging(level: int = logging.INFO, verbose: bool = True) -> None:
    """Configure the root logger with Rich handler for beautiful output.

    Args:
        level: Logging level (default: INFO)
        verbose: If True, use verbose format with timestamps and paths
    """
    # Configure Rich handler
    rich_handler = RichHandler(
        console=console,
        show_time=verbose,
        show_path=verbose,
        show_level=True,
        rich_tracebacks=True,
        tracebacks_show_locals=verbose,
        markup=True,
        log_time_format="[%X]",
    )

    rich_handler.setFormatter(logging.Formatter("%(message)s"))

    # Configure root logger
    logging.basicConfig(level=level, handlers=[rich_handler], force=True)


def get_logger(name: str, level: int | None = None) -> logging.Logger:
    """
    Get or create a logger with the specified name.

    Args:
        name: Name for the logger (typically __name__ or module name)
        level: Optional logging level override

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if level is not None:
        logger.setLevel(level)

    return logger


# Initialize default configuration when module is imported
configure_logging()
