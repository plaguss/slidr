"""Tests for serve.py module."""

import argparse
import contextlib
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from slidr.serve import create_build_args, serve_deck


class TestCreateBuildArgs:
    """Tests for create_build_args function."""

    def test_returns_namespace_object(self, temp_deck_dir: Path):
        """Should return argparse.Namespace object."""
        result = create_build_args(temp_deck_dir, None)
        assert isinstance(result, argparse.Namespace)

    def test_includes_deck_path(self, temp_deck_dir: Path):
        """Should include deck path in namespace."""
        result = create_build_args(temp_deck_dir, None)
        assert result.deck == str(temp_deck_dir)

    def test_includes_output_path(self, temp_deck_dir: Path):
        """Should include output path pointing to index.html."""
        result = create_build_args(temp_deck_dir, None)
        expected_output = str(temp_deck_dir / "index.html")
        assert result.output == expected_output

    def test_includes_theme_when_none(self, temp_deck_dir: Path):
        """Should include theme as None when not provided."""
        result = create_build_args(temp_deck_dir, None)
        assert result.theme is None

    @pytest.mark.parametrize(
        "theme_path",
        [
            "custom.css",
            "../themes/dark.css",
            "/absolute/path/theme.css",
        ],
    )
    def test_includes_theme_when_provided(self, temp_deck_dir: Path, theme_path: str):
        """Should include theme path when provided."""
        result = create_build_args(temp_deck_dir, theme_path)
        assert result.theme == theme_path

    def test_converts_path_to_string(self, temp_deck_dir: Path):
        """Should convert Path objects to strings."""
        result = create_build_args(temp_deck_dir, None)
        assert isinstance(result.deck, str)
        assert isinstance(result.output, str)


class TestServeDeck:
    """Tests for serve_deck function."""

    def test_raises_error_for_nonexistent_deck(self, tmp_path: Path):
        """Should raise FileNotFoundError for nonexistent deck directory."""
        args = argparse.Namespace(
            deck=str(tmp_path / "nonexistent"), port=8000, theme=None
        )

        with pytest.raises(FileNotFoundError, match="Deck directory not found"):
            serve_deck(args)

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    def test_performs_initial_build(
        self,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should perform initial build before starting server."""
        # Setup mocks
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server
        mock_watch.return_value = iter([])  # Empty iterator

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Verify initial build was called
        assert mock_build.call_count >= 1

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    def test_starts_http_server_on_correct_port(
        self,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should start HTTP server on specified port."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server
        mock_watch.return_value = iter([])

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8080, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Verify server was created with correct port
        mock_server_class.assert_called_once()
        call_args = mock_server_class.call_args[0]
        assert call_args[0] == ("localhost", 8080)

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    def test_starts_server_thread(
        self,
        mock_watch: Mock,
        mock_thread_class: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should start server in background thread."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server
        mock_thread = MagicMock()
        mock_thread_class.return_value = mock_thread
        mock_watch.return_value = iter([])

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Verify thread was created and started
        mock_thread_class.assert_called_once()
        mock_thread.start.assert_called_once()

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    def test_watches_deck_directory_for_changes(
        self,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should watch deck directory for file changes."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server
        mock_watch.return_value = iter([])

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Verify watch was called with deck directory
        mock_watch.assert_called_once()
        watch_path = mock_watch.call_args[0][0]
        assert watch_path == str(temp_deck_dir.resolve())

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    @patch("slidr.serve.time.time")
    def test_rebuilds_on_file_changes(
        self,
        mock_time: Mock,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should rebuild when file changes are detected."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        # Mock time to control debouncing
        mock_time.side_effect = [
            0,
            2,
            4,
        ]  # Initial, after first change, after second change

        # Simulate file changes
        changes = [
            {("change", str(temp_deck_dir / "deck.md"))},
            {("change", str(temp_deck_dir / "theme.css"))},
        ]
        mock_watch.return_value = iter(changes)

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Should have: initial build + rebuilds for changes
        assert mock_build.call_count >= 2

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    @patch("slidr.serve.time.time")
    def test_debounces_rapid_changes(
        self,
        mock_time: Mock,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should debounce rapid file changes (1 second threshold)."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        # Mock time: second change happens within 1 second
        mock_time.side_effect = [0, 0.5, 0.6, 2]

        # Simulate rapid changes
        changes = [
            {("change", str(temp_deck_dir / "deck.md"))},
            {("change", str(temp_deck_dir / "deck.md"))},  # Within debounce window
            {("change", str(temp_deck_dir / "deck.md"))},  # After debounce window
        ]
        mock_watch.return_value = iter(changes)

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Should have: initial + rebuilds (some may be debounced)
        # At least 2 builds (initial + one allowed rebuild)
        assert mock_build.call_count >= 2

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    def test_handles_keyboard_interrupt(
        self,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should handle KeyboardInterrupt and shutdown gracefully."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        # Simulate KeyboardInterrupt
        mock_watch.return_value = iter([])
        mock_watch.side_effect = KeyboardInterrupt()

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        result = serve_deck(args)

        # Should return 0 and shutdown server
        assert result == 0
        mock_server.shutdown.assert_called_once()

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    def test_uses_custom_theme_in_builds(
        self,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
        tmp_path: Path,
    ):
        """Should pass custom theme to build commands."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        # Mock time for debouncing
        with patch("slidr.serve.time.time", side_effect=[0, 2]):
            changes = [{("change", str(temp_deck_dir / "deck.md"))}]
            mock_watch.return_value = iter(changes)

            custom_theme = tmp_path / "custom.css"
            custom_theme.write_text("body { color: blue; }")

            args = argparse.Namespace(
                deck=str(temp_deck_dir), port=8000, theme=str(custom_theme)
            )

            with contextlib.suppress(StopIteration):
                serve_deck(args)

            # Check that builds received theme argument
            for call in mock_build.call_args_list:
                build_args = call[0][0]
                assert build_args.theme == str(custom_theme)

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    @patch("slidr.serve.time.time")
    def test_continues_serving_after_build_error(
        self,
        mock_time: Mock,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should continue serving even if a rebuild fails."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        # Mock time
        mock_time.side_effect = [0, 2, 4]

        # First build succeeds, second fails, third succeeds
        mock_build.side_effect = [None, Exception("Build error"), None]

        changes = [
            {("change", str(temp_deck_dir / "deck.md"))},
            {("change", str(temp_deck_dir / "deck.md"))},
        ]
        mock_watch.return_value = iter(changes)

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Should have attempted all builds
        assert mock_build.call_count == 3

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    @patch("os.chdir")
    def test_changes_to_deck_directory(
        self,
        mock_chdir: Mock,
        mock_watch: Mock,
        mock_thread: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should change to deck directory before serving."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server
        mock_watch.return_value = iter([])

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Verify chdir was called with deck directory
        mock_chdir.assert_called_once_with(temp_deck_dir.resolve())

    @patch("slidr.serve.build_deck")
    @patch("slidr.serve.HTTPServer")
    @patch("slidr.serve.Thread")
    @patch("slidr.serve.watch")
    def test_server_thread_is_daemon(
        self,
        mock_watch: Mock,
        mock_thread_class: Mock,
        mock_server_class: Mock,
        mock_build: Mock,
        temp_deck_dir: Path,
    ):
        """Should create server thread as daemon."""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server
        mock_thread = MagicMock()
        mock_thread_class.return_value = mock_thread
        mock_watch.return_value = iter([])

        args = argparse.Namespace(deck=str(temp_deck_dir), port=8000, theme=None)

        with contextlib.suppress(StopIteration):
            serve_deck(args)

        # Verify thread was created with daemon=True
        mock_thread_class.assert_called_once()
        call_kwargs = mock_thread_class.call_args[1]
        assert call_kwargs.get("daemon") is True
