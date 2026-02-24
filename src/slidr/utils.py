"""Common utility functions for Slidr."""

from pathlib import Path


def get_assets_dir() -> Path:
    """Get the path to the assets directory."""
    package_dir = Path(__file__).parent
    return package_dir / "assets"


def get_default_theme_path() -> Path:
    """Get the path to the default CSS theme."""
    return get_assets_dir() / "default.css"


def get_templates_dir() -> Path:
    """Get the path to the templates directory."""
    package_dir = Path(__file__).parent
    return package_dir / "templates"


def resolve_theme_path(theme_name: str, deck_dir: Path | None = None) -> Path | None:
    """
    Resolve a theme name to its full path.

    Checks in order:
    1. If theme_name is an absolute path, use it directly
    2. If theme_name exists as a file in deck_dir (if provided)
    3. If theme_name exists in assets directory (built-in themes)

    Args:
        theme_name: Name of the theme file (e.g., "gaia.css" or "gaia")
        deck_dir: Optional deck directory to check for custom themes

    Returns:
        Resolved Path to theme file, or None if not found
    """
    # Add .css extension if not present
    if not theme_name.endswith(".css"):
        theme_name = f"{theme_name}.css"

    theme_path = Path(theme_name)

    # Check if it's an absolute path
    if theme_path.is_absolute() and theme_path.exists():
        return theme_path

    # Check in deck directory
    if deck_dir:
        deck_theme = deck_dir / theme_name
        if deck_theme.exists():
            return deck_theme

    # Check in assets directory (built-in themes)
    asset_theme = get_assets_dir() / theme_name
    if asset_theme.exists():
        return asset_theme

    return None
