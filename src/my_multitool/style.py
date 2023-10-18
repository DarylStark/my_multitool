"""Styles for the application.

This module contains all the global styles for the application to give it a
consistent look.
"""

from rich.table import Table
from rich import box
from rich.console import Console


class ConsoleFactory:
    """Factory for a Rich Console."""

    global_console: Console | None = None

    @classmethod
    def get_console(cls) -> Console:
        """Create a Rich Console.

        Creates a Rich Console to use to display data. If a console is already
        created, it will return that console. Otherwise, it will create it and
        returns is.

        Returns:
            A Rich Conosle instance.
        """
        if not cls.global_console:
            cls.global_console = Console()
        return cls.global_console


def get_table() -> Table:
    """Create a Rich Table.

    Creates a Rich Table to use by functions that list data. By using a
    function for this, we can make sure all listing functions have the same
    look and feel.

    Returns:
        A Rich Table instance.
    """
    return Table(box=box.SIMPLE)


def print_error(message: str, prefix: str = 'Error') -> None:
    """Print a error message.

    Prints a error message in a Rich console. This can be used as a alternative
    to the Console.print method.

    Args:
        message: the error message.
        prefix: the prefix for the error message.
    """
    console = ConsoleFactory.get_console()
    console.print(f'[red][b]{prefix}:[/b] {message}')
