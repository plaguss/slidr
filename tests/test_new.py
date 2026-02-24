"""Tests for new.py module."""

import argparse
from pathlib import Path

import pytest

from slidr.new import init_project
from slidr.utils import get_default_theme_path


class TestGetDefaultThemePath:
    """Tests for get_default_theme_path function in utils module."""

    def test_returns_path_object(self):
        """Should return a Path object."""
        result = get_default_theme_path()
        assert isinstance(result, Path)

    def test_returns_default_css_path(self):
        """Should return path to default.css in assets directory."""
        result = get_default_theme_path()
        assert result.name == "default.css"
        assert result.parent.name == "assets"

    def test_default_theme_exists(self):
        """Should return a path that exists."""
        result = get_default_theme_path()
        assert result.exists()


class TestInitProject:
    """Tests for init_project function."""

    def test_creates_project_directory(self, tmp_path: Path):
        """Should create project directory."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        result = init_project(args)

        assert result == 0
        assert project_dir.exists()
        assert project_dir.is_dir()

    def test_creates_deck_subdirectory(self, tmp_path: Path):
        """Should create deck subdirectory inside project."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        deck_dir = project_dir / "deck"
        assert deck_dir.exists()
        assert deck_dir.is_dir()

    def test_creates_markdown_file_with_default_name(self, tmp_path: Path):
        """Should create markdown file with default name."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        md_file = project_dir / "deck" / "deck.md"
        assert md_file.exists()
        assert md_file.is_file()

    @pytest.mark.parametrize(
        "markdown_name",
        [
            "slides.md",
            "presentation.md",
            "my_slides.md",
        ],
    )
    def test_creates_markdown_file_with_custom_name(
        self, tmp_path: Path, markdown_name: str
    ):
        """Should create markdown file with custom name."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown=markdown_name)

        init_project(args)

        md_file = project_dir / "deck" / markdown_name
        assert md_file.exists()

    def test_markdown_file_has_default_content(self, tmp_path: Path):
        """Should populate markdown file with default slide content."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        md_file = project_dir / "deck" / "deck.md"
        content = md_file.read_text()

        assert "# Slide 1" in content
        assert "# Slide 2" in content
        assert "# Slide 3" in content
        assert "---" in content

    def test_markdown_content_has_three_slides(self, tmp_path: Path):
        """Should create markdown with three default slides."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        md_file = project_dir / "deck" / "deck.md"
        content = md_file.read_text()

        # Count slide separators
        separator_count = content.count("---")
        assert separator_count == 2  # 2 separators = 3 slides

    def test_copies_default_theme_to_deck(self, tmp_path: Path):
        """Should copy default theme.css to deck directory."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        theme_file = project_dir / "deck" / "theme.css"
        assert theme_file.exists()
        assert theme_file.is_file()

    def test_theme_file_has_css_content(self, tmp_path: Path):
        """Should copy CSS content to theme file."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        theme_file = project_dir / "deck" / "theme.css"
        content = theme_file.read_text()

        # Should contain CSS
        assert len(content) > 0
        assert content.strip()  # Not just whitespace

    def test_handles_existing_project_directory(self, tmp_path: Path):
        """Should not fail if project directory already exists."""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()

        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        result = init_project(args)
        assert result == 0

    def test_handles_existing_deck_directory(self, tmp_path: Path):
        """Should not fail if deck directory already exists."""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        deck_dir = project_dir / "deck"
        deck_dir.mkdir()

        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        result = init_project(args)
        assert result == 0

    def test_creates_nested_project_directories(self, tmp_path: Path):
        """Should create nested directories in project path."""
        project_dir = tmp_path / "parent" / "child" / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        result = init_project(args)

        assert result == 0
        assert project_dir.exists()
        assert (project_dir / "deck").exists()

    def test_returns_zero_exit_code(self, tmp_path: Path):
        """Should return 0 exit code on success."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        result = init_project(args)
        assert result == 0

    @pytest.mark.parametrize(
        "project_name",
        [
            "simple",
            "with-dashes",
            "with_underscores",
            "MixedCase",
            "project123",
        ],
    )
    def test_handles_various_project_names(self, tmp_path: Path, project_name: str):
        """Should handle various valid project name formats."""
        project_dir = tmp_path / project_name
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        result = init_project(args)

        assert result == 0
        assert project_dir.exists()

    def test_all_required_files_created(self, tmp_path: Path):
        """Should create all required files and directories."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        # Check all expected paths
        assert project_dir.exists()
        assert (project_dir / "deck").exists()
        assert (project_dir / "deck" / "deck.md").exists()
        assert (project_dir / "deck" / "theme.css").exists()

    def test_markdown_and_theme_files_are_files_not_directories(self, tmp_path: Path):
        """Should create files, not directories."""
        project_dir = tmp_path / "test_project"
        args = argparse.Namespace(project=str(project_dir), markdown="deck.md")

        init_project(args)

        assert (project_dir / "deck" / "deck.md").is_file()
        assert (project_dir / "deck" / "theme.css").is_file()
