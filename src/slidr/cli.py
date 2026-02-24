import argparse

from . import build, new, serve, themes
from .logging_utils import get_logger

logger = get_logger(__name__)


def create_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Slidr - Generate slides from markdown files", prog="slidr"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # new command
    new_parser = subparsers.add_parser(
        "new", help="Initialize a new slide deck project"
    )
    new_parser.add_argument("project", help="Project directory name")
    new_parser.add_argument(
        "-m",
        "--markdown",
        default="deck.md",
        help="Name of the markdown file (default: deck.md)",
    )
    new_parser.set_defaults(func=new.init_project)

    # build command
    build_parser = subparsers.add_parser("build", help="Build HTML from markdown")
    build_parser.add_argument(
        "deck",
        nargs="?",
        default=".",
        help="Path to the deck folder (default: current directory)",
    )
    build_parser.add_argument(
        "-o",
        "--output",
        help="Output HTML file path (default: index.html in deck directory)",
    )
    build_parser.add_argument(
        "-t",
        "--theme",
        help=(
            "Path to custom CSS theme (uses theme.css in deck if exists, "
            "otherwise default)"
        ),
    )
    build_parser.set_defaults(func=build.build_deck)

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Serve deck with file watching")
    serve_parser.add_argument(
        "deck",
        nargs="?",
        default=".",
        help="Path to the deck folder (default: current directory)",
    )
    serve_parser.add_argument(
        "-p", "--port", type=int, default=8000, help="Port to serve on (default: 8000)"
    )
    serve_parser.add_argument("-t", "--theme", help="Path to custom CSS theme")
    serve_parser.set_defaults(func=serve.serve_deck)

    # themes command
    themes_parser = subparsers.add_parser(
        "themes", help="List available default themes"
    )
    themes_parser.set_defaults(func=themes.list_themes)

    return parser


def main(args=None):
    """Main CLI entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not hasattr(parsed_args, "func"):
        parser.print_help()
        return 1

    try:
        return parsed_args.func(parsed_args)
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
