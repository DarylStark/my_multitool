"""Main entry point for the CLI script.

This module contains the `main()` method that exposes the CLI arguments for the
script. The CLI argument groups are imported from other modules.
"""
import logging
import sys

import typer
from my_data.exceptions import MyDataException  # type:ignore
from rich.logging import RichHandler

from .contexts import app as contexts_app
from .database import app as database_app
from .exceptions import (ConfigFileNotFoundException,
                         ConfigFileNotValidException, GenericCLIException)
from .globals import config
from .style import print_error
from .users import app as users_app


def main() -> None:
    """Entry point for the CLI script.

    Defines the commands for the CLI script and makes sure the correct
    functions get called when running a specific CLI command.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()])
    logger = logging.getLogger('MAIN')

    # Load the configurationfile
    config.configure('~/.my_multitool_config.yaml')
    try:
        config.load()
    except ConfigFileNotFoundException:
        logger.warning(
            'Configurationfile did not exist. Creating default configuration.')
        config.set_default_config()
        config.save()
    except ConfigFileNotValidException:
        logging.error('Configurationfile not valid')
        sys.exit(1)

    # Create the Typer App
    app = typer.Typer(no_args_is_help=True)

    # Add subcommand's
    app.add_typer(database_app, name='database', help='Database management')
    app.add_typer(contexts_app, name='contexts', help='Context management')
    app.add_typer(users_app, name='users', help='User management')

    # Run the Typer app
    try:
        app()
    except GenericCLIException as exception:
        print_error(str(exception), prefix='CLI error')
    except MyDataException as exception:
        print_error(str(exception), prefix='MyData error')


if __name__ == '__main__':
    main()
