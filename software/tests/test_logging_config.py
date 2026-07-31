"""Tests for batch_processing.logging_config.

setup_logging() is called by two pipeline entry points
(scripts/generate_all_outputs.py, scripts/import_legacy_materials.py) but
had no direct unit test; subprocess-based CLI tests exercise it
transitively without pytest-cov measuring it or asserting anything about
the logger's actual configuration.
"""

import logging

from src.batch_processing.logging_config import get_logger, setup_logging


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_creates_log_file_under_log_dir(self, temp_dir):
        """A timestamped log file is created under the given log_dir."""
        logger = setup_logging(log_dir=temp_dir)

        log_files = list(temp_dir.glob("generation_*.log"))
        assert len(log_files) == 1
        assert log_files[0].exists()
        # Sanity check the naming pattern: generation_YYYY-MM-DD_HH-MM-SS.log
        assert log_files[0].name.startswith("generation_")
        assert log_files[0].suffix == ".log"

        logger.handlers.clear()

    def test_attaches_exactly_two_handlers_with_expected_levels(self, temp_dir):
        """Exactly one console (StreamHandler) and one file (FileHandler)
        handler are attached, with console at log_level and file at
        file_level."""
        logger = setup_logging(
            log_dir=temp_dir, log_level=logging.WARNING, file_level=logging.DEBUG
        )

        assert len(logger.handlers) == 2
        stream_handlers = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(stream_handlers) == 1
        assert len(file_handlers) == 1
        assert stream_handlers[0].level == logging.WARNING
        assert file_handlers[0].level == logging.DEBUG

        logger.handlers.clear()

    def test_logger_level_captures_all_and_handlers_filter(self, temp_dir):
        """The logger itself is set to DEBUG (capture everything); handlers
        are responsible for filtering to their own levels."""
        logger = setup_logging(log_dir=temp_dir)

        assert logger.level == logging.DEBUG

        logger.handlers.clear()

    def test_repeated_calls_do_not_accumulate_duplicate_handlers(self, temp_dir):
        """Calling setup_logging() twice on the same logger name must not
        accumulate duplicate handlers (the explicit logger.handlers.clear()
        call exists to guarantee this)."""
        logger1 = setup_logging(log_dir=temp_dir)
        assert len(logger1.handlers) == 2

        logger2 = setup_logging(log_dir=temp_dir)
        assert len(logger2.handlers) == 2
        assert logger1 is logger2  # same named logger instance

        logger2.handlers.clear()

    def test_default_log_dir_defaults_under_software_logs(self):
        """When log_dir is omitted, the log file is created under
        software/logs/ relative to this module (not, e.g., cwd)."""
        logger = setup_logging()
        try:
            file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
            assert len(file_handlers) == 1
            log_path = file_handlers[0].baseFilename
            assert "logs" in log_path
            assert "generation_" in log_path
        finally:
            logger.handlers.clear()


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_logger_with_default_name(self):
        logger = get_logger()
        assert logger.name == "batch_processing"

    def test_returns_logger_with_custom_name(self):
        logger = get_logger("custom_name")
        assert logger.name == "custom_name"
