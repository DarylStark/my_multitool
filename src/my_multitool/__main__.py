"""Main entry point for the CLI script.

This module contains the `main()` method that exposes the CLI arguments for the
script. The CLI argument groups are imported from other modules.
"""
import logging
import sys

import typer
from my_data import __version__ as my_data_version
from my_data.exceptions import MyDataException
from my_model import __version__ as my_model_version
from pydantic import __version__ as pydantic_version
from rich.logging import RichHandler
from sqlalchemy import __version__ as sqlalchemy_version
from sqlmodel import __version__ as sqlmodel_version
from typer import __version__ as typer_version

from . import __version__ as my_multitool_version
from .cli_config import app as config_app
from .cli_database import app as database_app
from .cli_users import app as users_app
from .exceptions import (ConfigFileNotFoundException,
                         ConfigFileNotValidException, GenericCLIException,
                         NoConfirmationException, SQLError)
from .globals import config
from .style import ConsoleFactory, get_table, print_error

# Create the Typer App
app = typer.Typer(no_args_is_help=True)


@app.command(name='version')
def version() -> None:
    """Display version information.

    Shows version information for the tool and all related libraries.
    """
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


# Add subcommand's
app.add_typer(database_app, name='database', help='Database management')
app.add_typer(users_app, name='users', help='User management')
app.add_typer(config_app, name='config', help='Configuration for My Multitool')


def main() -> int:  # pragma: no cover
    """Entry point for the CLI script.

    Defines the commands for the CLI script and makes sure the correct
    functions get called when running a specific CLI command.

    Returns:
        The return code for the program. The calling code should use this as
        the exit code for the application.
    """
    # Load the configurationfile
    config.configure('~/.my_multitool_config.yaml')
    try:
        config.load()
    except ConfigFileNotFoundException:
        config.set_default_config()
        config.save()
    except ConfigFileNotValidException:
        print_error('Configurationfile not valid', prefix='Configuration')
        sys.exit(1)

    # Configure logging
    logging.basicConfig(
        level=config.config.logging_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()])
    logger = logging.getLogger('MAIN')
    logger.debug('Logging is configured!')

    # Run the Typer app
    try:
        app()
    except NoConfirmationException as exception:
        print_error(str(exception), prefix='CLI error')
        return 1
    except GenericCLIException as exception:
        print_error(str(exception), prefix='CLI error')
        return 2
    except SQLError as exception:
        print_error(str(exception), prefix='SQL error')
        return 4
    except MyDataException as exception:
        print_error(str(exception), prefix='MyData error')
        return 8
    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
