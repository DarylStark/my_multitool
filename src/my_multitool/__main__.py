"""Main entry point for the CLI script.

This module contains the `main()` method that exposes the CLI arguments for the
script. The CLI argument groups are imported from other modules.
"""
import logging
import sys

import typer
from rich.logging import RichHandler

from .config import ConfigManager
from .contexts import app as contexts_app
from .database import app as database_app
from .exceptions import (ConfigFileNotFoundException,
                         ConfigFileNotValidException)


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
    cfg = ConfigManager('~/.my_multitool_config.yaml')
    try:
        cfg.load()
    except ConfigFileNotFoundException:
        logging.warning(
            'Configurationfile did not exist. Creating default configuration.')
        cfg.set_default_config()
        cfg.save()
    except ConfigFileNotValidException:
        logging.error('Configurationfile not valid')
        sys.exit(1)

    # Create the Typer App
    app = typer.Typer(no_args_is_help=True)

    # Add subcommand's
    app.add_typer(database_app, name='database', help='Database management')
    app.add_typer(contexts_app, name='contexts', help='Context management')

    # Run the Typer app
    app()


if __name__ == '__main__':
    main()
