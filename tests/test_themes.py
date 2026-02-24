"""Tests for the themes command."""

import argparse

from slidr.cli import create_parser
from slidr.themes import list_themes
from slidr.utils import get_assets_dir


def test_list_themes_shows_all_default_themes(caplog):
    """Test that list_themes displays all available default themes."""
    args = argparse.Namespace()

    result = list_themes(args)

    assert result == 0

    # Check that the log contains expected themes
    log_output = caplog.text
    assert "Available default themes:" in log_output

    # Verify some known themes are listed
    expected_themes = ["academic", "default", "dark-professional", "minimal-light"]
    for theme in expected_themes:
        assert theme in log_output

    # Check usage hint is provided
    assert "Use with: slidr build deck --theme" in log_output


def test_list_themes_shows_actual_asset_files():
    """Test that list_themes shows all CSS files from assets directory."""
    args = argparse.Namespace()
    assets_dir = get_assets_dir()

    # Get actual theme files
    theme_files = list(assets_dir.glob("*.css"))
    assert len(theme_files) > 0, "Should have at least one theme file"

    result = list_themes(args)

    assert result == 0


def test_themes_command_parser():
    """Test that themes command is properly configured in parser."""
    parser = create_parser()
    args = parser.parse_args(["themes"])

    assert args.command == "themes"
    assert hasattr(args, "func")
    assert args.func.__name__ == "list_themes"
