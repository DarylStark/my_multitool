"""Module with models for the specific application.

Contains moduls for the My Multitool application.
"""
from enum import Enum


class LoggingLevel(str, Enum):
    """Enum with the specific debugging levels.

    Will be used by the Typer app to give the user a choice in how much logging
    he wishes.
    """

    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    FATAL = 'fatal'

    def __int__(self) -> int:
        """Return the integer value for the chosen level.

        The enum will contain a string indicating the selected logging level.
        This is needed for Typer, but for the logging module we need a integer.
        This method converts the string that is needed for Typer to the integer
        that is needed for the Logging module.

        Returns:
            The integer value for the chosen value. If the integer for the
            value cannot be found, it returns '20', which indicates a default
            value for the `info` value.
        """
        levels = {
            'debug': 10, 'info': 20, 'warning': 30, 'error': 40, 'fatal': 50
        }
        return levels.get(self.value, 10)
