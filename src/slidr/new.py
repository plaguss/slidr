"""Initialize a new slide deck project."""

import argparse
import shutil
from pathlib import Path

from .logging_utils import get_logger
from .utils import get_default_theme_path

logger = get_logger(__name__)


def init_project(args: argparse.Namespace) -> int:
    """
    Initialize a new slide deck project.

    Args:
        args: Parsed command-line arguments containing:
            - project: Project directory name
            - markdown: Name of the markdown file

    Returns:
        Exit code (0 for success)
    """
    project_dir = Path(args.project)

    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create deck subdirectory
    deck_dir = project_dir / "deck"
    deck_dir.mkdir(exist_ok=True)

    # Create markdown file
    md_file = deck_dir / args.markdown
    md_file.write_text("""# Slide 1
Your first slide content here.

---

# Slide 2
Your second slide content here.

---

# Slide 3
Your third slide content here.
""")

    # Copy default theme
    theme_file = deck_dir / "theme.css"
    shutil.copy(get_default_theme_path(), theme_file)

    logger.info(f"✓ Project initialized at {project_dir}")
    logger.info(f"✓ Created deck folder with {args.markdown} and theme.css")
    logger.info("")
    logger.info("Next steps:")
    logger.info(f"  cd {project_dir}")
    logger.info("  slidr build deck")
    logger.info("  slidr serve deck")

    return 0
