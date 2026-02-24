"""Command to list available themes."""

import argparse

from slidr.logging_utils import get_logger
from slidr.utils import get_assets_dir

logger = get_logger(__name__)


def list_themes(args: argparse.Namespace) -> int:
    """
    List all available default themes.

    Args:
        args: Command-line arguments from argparse

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    assets_dir = get_assets_dir()

    # Get all CSS files from the assets directory
    theme_files = sorted(assets_dir.glob("*.css"))

    if not theme_files:  # pragma: no cover
        logger.warning("No themes found in assets directory")
        return 1

    logger.info("Available default themes:")
    for theme_file in theme_files:
        theme_name = theme_file.stem
        logger.info(f"  - {theme_name}")

    logger.info(f"\nUse with: slidr build deck --theme {theme_files[0].stem}")

    return 0
