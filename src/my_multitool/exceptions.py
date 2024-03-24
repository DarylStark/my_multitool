"""Module with exceptions.

Module that contains all the exceptions for the My Multitool tool.
"""


class MyMultitoolError(Exception):
    """Base exception for My Multutool."""


class ConfigFileNotFoundError(MyMultitoolError):
    """Exception for when the configfile doesn't exist."""


class ConfigFileNotValidError(MyMultitoolError):
    """Exception for when the configfile is invalid."""


class NoConfigToSaveError(MyMultitoolError):
    """Exception for a config is saved before loading it."""


class GenericCLIError(MyMultitoolError):
    """Exception for a generic error in the CLI options."""


class NoConfirmationError(MyMultitoolError):
    """Exception when the user presses N at a confirmation."""


class SQLError(MyMultitoolError):
    """Exception for a SQL error."""
