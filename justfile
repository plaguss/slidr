set shell := ["cmd.exe", "/c"]
# Slidr project justfile
# Run `just --list` to see all available commands

# Default recipe
default:
    @just --list

# Install the package in editable mode
install:
    uv pip install -e .

# Install development dependencies
install-dev:
    uv pip install -e ".[dev]"

# Install pre-commit hooks
install-hooks:
    pre-commit install

# Run all tests with coverage report
test:
    pytest

# Format code with ruff
fmt:
    ruff format src/slidr tests

# Run linter with fix
lint:
    ruff check --fix src/slidr tests

# Run type checking with ty
typecheck:
    ty check

# Run both linter and formatter checks
check: lint fmt typecheck

# Run pre-commit on all files
pre-commit-run:
    pre-commit run --all-files

# Build the sample deck
build:
    slidr build deck

# Serve the sample deck (runs on port 8000 by default)
serve PORT="8000":
    slidr serve deck -p {{ PORT }}

# Development setup: install package, dev deps, and pre-commit hooks
dev-setup: install-dev install-hooks
    @echo "Development environment is ready!"
    @echo "Run 'just serve' to start the development server"

# Clean build artifacts
clean:
    rm -rf build/ dist/ *.egg-info htmlcov/ .coverage .pytest_cache __pycache__/

# Clean and rebuild
rebuild: clean build
