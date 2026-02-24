"""Shared pytest fixtures for slidr tests."""

from pathlib import Path

import pytest


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture
def temp_deck_dir(tmp_path: Path) -> Path:
    """Create a temporary deck directory with a markdown file."""
    deck_dir = tmp_path / "deck"
    deck_dir.mkdir()

    # Create a sample markdown file
    md_file = deck_dir / "deck.md"
    md_file.write_text("""# Slide 1
First slide content.

---

# Slide 2
Second slide content.

---

# Slide 3
Third slide content.
""")

    return deck_dir


@pytest.fixture
def temp_deck_dir_with_theme(temp_deck_dir: Path) -> Path:
    """Create a temporary deck directory with markdown and custom theme."""
    theme_file = temp_deck_dir / "theme.css"
    theme_file.write_text("""
body {
    background: red;
}
""")
    return temp_deck_dir


@pytest.fixture
def sample_markdown_content() -> str:
    """Return sample markdown content with multiple slides."""
    return """# First Slide
Content here.

---

# Second Slide
More content.

---

# Third Slide
Final content.
"""


@pytest.fixture
def sample_css_content() -> str:
    """Return sample CSS content."""
    return """
body {
    background: #fff;
    color: #000;
}

.slide {
    padding: 20px;
}
"""


@pytest.fixture
def empty_deck_dir(tmp_path: Path) -> Path:
    """Create an empty deck directory (no markdown files)."""
    deck_dir = tmp_path / "empty_deck"
    deck_dir.mkdir()
    return deck_dir


@pytest.fixture
def temp_deck_dir_with_front_matter(tmp_path: Path) -> Path:
    """Create a temporary deck directory with front matter in markdown."""
    deck_dir = tmp_path / "deck_with_fm"
    deck_dir.mkdir()

    # Create a markdown file with front matter
    md_file = deck_dir / "deck.md"
    md_file.write_text("""---
theme: custom
title: My Awesome Presentation
---

# Slide 1
First slide content.

---

# Slide 2
Second slide content.
""")

    # Create the custom theme referenced in front matter
    theme_file = deck_dir / "custom.css"
    theme_file.write_text("body { background: purple; }")

    return deck_dir
