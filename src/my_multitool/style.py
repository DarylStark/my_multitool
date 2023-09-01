"""Styles for the application.

This module contains all the global styles for the application to give it a
consistent look.
"""

from rich.table import Table
from rich import box


def table_factory() -> Table:
    """Function to create a Rich Table.

    Creates a Rich Table to use by functions that list data. By using a
    function for this, we can make sure all listing functions have the same
    look and feel.
    """
    return Table(box=box.SIMPLE)
