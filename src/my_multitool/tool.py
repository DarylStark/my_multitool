"""The `tool` portion of the CLI app.

Exposes the `tool` commands for the CLI app.
"""
from logging import getLogger

import typer

from .style import get_table, ConsoleFactory

from . import __version__ as my_multitool_version
from my_data import __version__ as my_data_version
from my_model import __version__ as my_model_version
from pydantic import __version__ as pydantic_version
from sqlmodel import __version__ as sqlmodel_version
from sqlalchemy import __version__ as sqlalchemy_version
from typer import __version__ as typer_version


app = typer.Typer(no_args_is_help=True)


@app.command(name='version')
def version() -> None:
    """Display version information.

    Shows version information for the tool and all related libraries.
    """
    logger = getLogger('tool-version')
    console = ConsoleFactory.get_console()

    table = get_table()
    table.add_column('Library')
    table.add_column('Version')
    
    table.add_row('My Model', my_model_version)
    table.add_row('My Data', my_data_version)
    table.add_row('My Multitool', my_multitool_version)
    table.add_row('Pydantic', pydantic_version)
    table.add_row('SQLModel', sqlmodel_version)
    table.add_row('SQLAlchemy', sqlalchemy_version)
    table.add_row('Typer', typer_version)

    console.print(table)