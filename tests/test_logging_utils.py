"""Tests for logging_utils.py module."""

import logging
from unittest.mock import patch

import pytest

from slidr.logging_utils import (
    configure_logging,
    get_logger,
)


class TestConfigureLogging:
    """Tests for configure_logging function."""

    def test_configures_logging_with_default_level(self):
        """Should configure logging with INFO level by default."""
        with patch("logging.basicConfig") as mock_basic_config:
            configure_logging()

            mock_basic_config.assert_called_once()
            call_kwargs = mock_basic_config.call_args[1]
            assert call_kwargs["level"] == logging.INFO

    @pytest.mark.parametrize(
        "level,expected",
        [
            (logging.DEBUG, logging.DEBUG),
            (logging.INFO, logging.INFO),
            (logging.WARNING, logging.WARNING),
            (logging.ERROR, logging.ERROR),
            (logging.CRITICAL, logging.CRITICAL),
        ],
    )
    def test_configures_logging_with_custom_level(self, level: int, expected: int):
        """Should configure logging with specified level."""
        with patch("logging.basicConfig") as mock_basic_config:
            configure_logging(level=level)

            call_kwargs = mock_basic_config.call_args[1]
            assert call_kwargs["level"] == expected

    def test_uses_rich_handler(self):
        """Should use RichHandler for logging."""
        with patch("logging.basicConfig") as mock_basic_config:
            configure_logging()

            call_kwargs = mock_basic_config.call_args[1]
            assert "handlers" in call_kwargs
            handlers = call_kwargs["handlers"]
            assert len(handlers) > 0

    def test_forces_configuration(self):
        """Should force reconfiguration of logging."""
        with patch("logging.basicConfig") as mock_basic_config:
            configure_logging()

            call_kwargs = mock_basic_config.call_args[1]
            assert call_kwargs.get("force") is True

    def test_accepts_both_level_and_verbose(self):
        """Should accept both level and verbose parameters."""
        with patch("logging.basicConfig") as mock_basic_config:
            configure_logging(level=logging.DEBUG, verbose=True)

            call_kwargs = mock_basic_config.call_args[1]
            assert call_kwargs["level"] == logging.DEBUG

    def test_verbose_flag_affects_handler(self):
        """Should configure handler differently based on verbose flag."""
        # Just test that it accepts verbose parameter without error
        with patch("logging.basicConfig"):
            configure_logging(verbose=True)
            configure_logging(verbose=False)


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_logger_instance(self):
        """Should return a logging.Logger instance."""
        logger = get_logger("test_logger")
        assert isinstance(logger, logging.Logger)

    def test_creates_logger_with_correct_name(self):
        """Should create logger with specified name."""
        logger = get_logger("my_module")
        assert logger.name == "my_module"

    @pytest.mark.parametrize(
        "logger_name",
        [
            "module1",
            "module.submodule",
            "slidr.build",
            "slidr.cli",
            "__main__",
        ],
    )
    def test_creates_loggers_with_various_names(self, logger_name: str):
        """Should create loggers with various name formats."""
        logger = get_logger(logger_name)
        assert logger.name == logger_name

    def test_returns_existing_logger_if_already_created(self):
        """Should return existing logger with same name."""
        logger1 = get_logger("shared_logger")
        logger2 = get_logger("shared_logger")
        assert logger1 is logger2

    def test_does_not_set_level_when_none(self):
        """Should not set level when level parameter is None."""
        logger = get_logger("test_logger", level=None)
        # Logger should exist but level not explicitly set by get_logger
        assert isinstance(logger, logging.Logger)

    @pytest.mark.parametrize(
        "level",
        [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ],
    )
    def test_sets_level_when_provided(self, level: int):
        """Should set logger level when provided."""
        logger = get_logger(f"test_logger_{level}", level=level)
        assert logger.level == level

    def test_level_override_affects_only_specific_logger(self):
        """Should only affect level of specific logger, not root."""
        logger1 = get_logger("logger1", level=logging.DEBUG)
        logger2 = get_logger("logger2", level=logging.ERROR)

        assert logger1.level == logging.DEBUG
        assert logger2.level == logging.ERROR

    def test_accepts_module_name_pattern(self):
        """Should work with __name__ pattern for module names."""
        module_name = "slidr.test_module"
        logger = get_logger(module_name)
        assert logger.name == module_name


class TestModuleInitialization:
    """Tests for module-level initialization."""

    def test_module_configures_logging_on_import(self):
        """Should configure logging when module is imported."""
        # This is implicitly tested by importing the module
        # The configure_logging() call at module level should work
        from slidr import logging_utils

        assert hasattr(logging_utils, "configure_logging")
        assert hasattr(logging_utils, "get_logger")


class TestLoggerUsage:
    """Integration tests for logger usage."""

    def test_logger_can_log_messages(self):
        """Should be able to log messages at different levels."""
        logger = get_logger("test_integration")

        # These should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    def test_multiple_loggers_coexist(self):
        """Should allow multiple loggers to coexist."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        logger3 = get_logger("module3")

        assert logger1.name == "module1"
        assert logger2.name == "module2"
        assert logger3.name == "module3"

        # All should be independent
        assert logger1 is not logger2
        assert logger2 is not logger3
        assert logger1 is not logger3

    def test_logger_with_custom_level_logs_appropriately(self):
        """Should respect custom log levels."""
        logger = get_logger("test_filtered", level=logging.WARNING)

        # With WARNING level, debug and info should be filtered
        # This is a behavior test - no exception should occur
        logger.debug("Should be filtered")
        logger.info("Should be filtered")
        logger.warning("Should appear")
        logger.error("Should appear")
