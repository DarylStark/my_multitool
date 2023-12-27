"""Tests for the model.

Tests the model for the `my-multitool` library.
"""
import logging

import pytest

from my_multitool.models import LoggingLevel


@pytest.mark.parametrize('level_object, level_value', [
    (LoggingLevel.DEBUG, logging.DEBUG),
    (LoggingLevel.INFO, logging.INFO),
    (LoggingLevel.WARNING, logging.WARNING),
    (LoggingLevel.ERROR, logging.ERROR),
    (LoggingLevel.FATAL, logging.FATAL)
])
def test_logging_levels(level_object: str, level_value: int) -> None:
    """Test if the logging levels match the `logging` module.

    The LoggingLevel contains levels that should match the integers from the
    `logging` module.
    """
    assert int(level_object) == level_value
