"""The `config` portion of the app."""
import logging

import typer

from .cli_config_contexts import app as contexts_app
from .globals import config
from .models import LoggingLevel
from .style import ConsoleFactory

app = typer.Typer(no_args_is_help=True)


@app.command(name='set-logging-level')
def set_logging_level(level: LoggingLevel) -> None:
    """Set logging level.

    Args:
        level: the logging level to set.

    Sets the logging level for the application. This will be saved in the
    configurationfile.
    """
    logger = logging.getLogger('set_logging_level')
    console = ConsoleFactory.get_console()
    logger.debug('Logging level "%s" is %d in integer', level, int(level))
    config.config.logging_level = int(level)
    config.save()
    console.print('Logging level set')


app.add_typer(contexts_app, name='contexts', help='Context management')
