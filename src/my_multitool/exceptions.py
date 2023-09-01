"""Module with exceptions.

Module that contains all the exceptions for the My Multitool tool.
"""


class MyMultitoolException(Exception):
    """Base exception for My Multutool."""


class ConfigFileNotFoundException(MyMultitoolException):
    """Exception for when the configfile doesn't exist."""


class ConfigFileNotValidException(MyMultitoolException):
    """Exception for when the configfile is invalid."""


class NoConfigToSaveException(MyMultitoolException):
    """Exception for a config is saved before loading it."""


class GenericCLIException(MyMultitoolException):
    """Exception for a generic error in the CLI options."""
