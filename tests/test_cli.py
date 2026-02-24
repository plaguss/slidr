"""Tests for cli.py module."""

import argparse
from unittest.mock import patch

import pytest

from slidr.cli import create_parser, main


class TestCreateParser:
    """Tests for create_parser function."""

    def test_returns_argument_parser(self):
        """Should return an ArgumentParser object."""
        parser = create_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_parser_has_command_subparsers(self):
        """Should have subparsers for commands."""
        parser = create_parser()
        # Parser should have subparsers
        args = parser.parse_args([])
        # No command specified means func attribute won't exist
        assert not hasattr(args, "func") or args.command is None

    @pytest.mark.parametrize("command", ["new", "build", "serve", "themes"])
    def test_parser_supports_all_commands(self, command: str):
        """Should support new, build, serve, and themes commands."""
        parser = create_parser()

        # Each command should parse without error
        if command == "new":
            args = parser.parse_args([command, "test_project"])
            assert args.command == command
        elif command == "build" or command == "serve":
            args = parser.parse_args([command])
            assert args.command == command
        else:  # themes
            args = parser.parse_args([command])
            assert args.command == command


class TestNewCommand:
    """Tests for new command parser."""

    def test_new_requires_project_argument(self):
        """Should require project argument."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["new"])

    def test_new_parses_project_name(self):
        """Should parse project name argument."""
        parser = create_parser()
        args = parser.parse_args(["new", "my_project"])

        assert args.project == "my_project"

    def test_new_has_default_markdown_name(self):
        """Should have default markdown file name."""
        parser = create_parser()
        args = parser.parse_args(["new", "test"])

        assert args.markdown == "deck.md"

    @pytest.mark.parametrize(
        "markdown_name",
        [
            "slides.md",
            "presentation.md",
            "my_deck.md",
        ],
    )
    def test_new_accepts_custom_markdown_name(self, markdown_name: str):
        """Should accept custom markdown file name with --markdown flag."""
        parser = create_parser()
        args = parser.parse_args(["new", "test", "--markdown", markdown_name])

        assert args.markdown == markdown_name

    def test_new_has_func_attribute(self):
        """Should have func attribute set to init_project."""
        parser = create_parser()
        args = parser.parse_args(["new", "test"])

        assert hasattr(args, "func")
        assert args.func.__name__ == "init_project"


class TestBuildCommand:
    """Tests for build command parser."""

    def test_build_has_default_deck_path(self):
        """Should have default deck path as current directory."""
        parser = create_parser()
        args = parser.parse_args(["build"])

        assert args.deck == "."

    def test_build_accepts_deck_argument(self):
        """Should accept deck path argument."""
        parser = create_parser()
        args = parser.parse_args(["build", "my_deck"])

        assert args.deck == "my_deck"

    def test_build_output_default_is_none(self):
        """Should have None as default output."""
        parser = create_parser()
        args = parser.parse_args(["build"])

        assert args.output is None

    @pytest.mark.parametrize(
        "output_path",
        [
            "output.html",
            "../output/slides.html",
            "dist/index.html",
        ],
    )
    def test_build_accepts_output_flag(self, output_path: str):
        """Should accept --output flag."""
        parser = create_parser()
        args = parser.parse_args(["build", "--output", output_path])

        assert args.output == output_path

    def test_build_theme_default_is_none(self):
        """Should have None as default theme."""
        parser = create_parser()
        args = parser.parse_args(["build"])

        assert args.theme is None

    @pytest.mark.parametrize(
        "theme_path",
        [
            "custom.css",
            "../themes/dark.css",
            "my_theme.css",
        ],
    )
    def test_build_accepts_theme_flag(self, theme_path: str):
        """Should accept --theme flag."""
        parser = create_parser()
        args = parser.parse_args(["build", "--theme", theme_path])

        assert args.theme == theme_path

    def test_build_accepts_multiple_flags(self):
        """Should accept multiple flags together."""
        parser = create_parser()
        args = parser.parse_args(
            ["build", "my_deck", "--output", "out.html", "--theme", "theme.css"]
        )

        assert args.deck == "my_deck"
        assert args.output == "out.html"
        assert args.theme == "theme.css"

    def test_build_has_func_attribute(self):
        """Should have func attribute set to build_deck."""
        parser = create_parser()
        args = parser.parse_args(["build"])

        assert hasattr(args, "func")
        assert args.func.__name__ == "build_deck"


class TestServeCommand:
    """Tests for serve command parser."""

    def test_serve_has_default_deck_path(self):
        """Should have default deck path as current directory."""
        parser = create_parser()
        args = parser.parse_args(["serve"])

        assert args.deck == "."

    def test_serve_accepts_deck_argument(self):
        """Should accept deck path argument."""
        parser = create_parser()
        args = parser.parse_args(["serve", "my_deck"])

        assert args.deck == "my_deck"

    def test_serve_has_default_port(self):
        """Should have default port 8000."""
        parser = create_parser()
        args = parser.parse_args(["serve"])

        assert args.port == 8000

    @pytest.mark.parametrize("port", [3000, 8080, 5000, 9000])
    def test_serve_accepts_port_flag(self, port: int):
        """Should accept --port flag with integer value."""
        parser = create_parser()
        args = parser.parse_args(["serve", "--port", str(port)])

        assert args.port == port

    def test_serve_theme_default_is_none(self):
        """Should have None as default theme."""
        parser = create_parser()
        args = parser.parse_args(["serve"])

        assert args.theme is None

    def test_serve_accepts_theme_flag(self):
        """Should accept --theme flag."""
        parser = create_parser()
        args = parser.parse_args(["serve", "--theme", "custom.css"])

        assert args.theme == "custom.css"

    def test_serve_accepts_multiple_flags(self):
        """Should accept multiple flags together."""
        parser = create_parser()
        args = parser.parse_args(
            ["serve", "my_deck", "--port", "3000", "--theme", "theme.css"]
        )

        assert args.deck == "my_deck"
        assert args.port == 3000
        assert args.theme == "theme.css"

    def test_serve_has_func_attribute(self):
        """Should have func attribute set to serve_deck."""
        parser = create_parser()
        args = parser.parse_args(["serve"])

        assert hasattr(args, "func")
        assert args.func.__name__ == "serve_deck"


class TestMain:
    """Tests for main function."""

    def test_main_returns_0_for_successful_command(self, temp_deck_dir):
        """Should return 0 when command executes successfully."""
        with patch("slidr.cli.build.build_deck", return_value=0):
            result = main(["build", str(temp_deck_dir)])
            assert result == 0

    def test_main_returns_1_when_no_command_provided(self):
        """Should return 1 when no command is provided."""
        result = main([])
        assert result == 1

    def test_main_returns_1_on_command_exception(self, temp_deck_dir):
        """Should return 1 when command raises exception."""
        with patch("slidr.cli.build.build_deck", side_effect=Exception("Test error")):
            result = main(["build", str(temp_deck_dir)])
            assert result == 1

    def test_main_catches_file_not_found_error(self):
        """Should catch FileNotFoundError and return 1."""
        result = main(["build", "/nonexistent/path"])
        assert result == 1

    def test_main_calls_new_command(self):
        """Should call new command function."""
        with patch("slidr.cli.new.init_project", return_value=0) as mock_init:
            result = main(["new", "test_project"])

            mock_init.assert_called_once()
            assert result == 0

    def test_main_calls_build_command(self):
        """Should call build command function."""
        with patch("slidr.cli.build.build_deck", return_value=0) as mock_build:
            result = main(["build"])

            mock_build.assert_called_once()
            assert result == 0

    def test_main_calls_serve_command(self):
        """Should call serve command function."""
        with patch("slidr.cli.serve.serve_deck", return_value=0) as mock_serve:
            result = main(["serve"])

            mock_serve.assert_called_once()
            assert result == 0

    @pytest.mark.parametrize(
        "command_args,expected_func,module_name",
        [
            (["new", "test"], "init_project", "new"),
            (["build"], "build_deck", "build"),
            (["serve"], "serve_deck", "serve"),
        ],
    )
    def test_main_dispatches_to_correct_function(
        self, command_args, expected_func, module_name
    ):
        """Should dispatch to correct function for each command."""
        with patch(
            f"slidr.cli.{module_name}.{expected_func}", return_value=0
        ) as mock_func:
            main(command_args)
            mock_func.assert_called_once()

    def test_main_with_none_args_uses_sys_argv(self):
        """Should use sys.argv when args is None."""
        with (
            patch("sys.argv", ["slidr", "build"]),
            patch("slidr.cli.build.build_deck", return_value=0) as mock_build,
        ):
            result = main()
            assert result == 0
            mock_build.assert_called_once()
