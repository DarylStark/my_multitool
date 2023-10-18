"""The `database` portion of the CLI app.

Exposes the `database` commands for the CLI app.
"""
from logging import getLogger

import typer

from .globals import config, get_global_data_object
from .style import ConsoleFactory

app = typer.Typer(no_args_is_help=True)


@app.command(name='create')
def create(echo_sql: bool = False,
           drop_tables: bool = False,
           create_data: bool = False) -> None:
    """Create the database schema.

    Creates the database schema for the currently activated context.

    Args:
        echo_sql: if set to True, the SQL queries that are executed will be
            displayed. This can be usefull to see what is happening.
        drop_tables: if set to True, all tables will be dropped which will
            result in data loss.
        create_data: if set to True, testdata will be created.
    """
    logger = getLogger('database-create')
    console = ConsoleFactory.get_console()
    logger.info('Using config "%s"', config.active_context.name)

    if config.active_context.warning:
        logger.warning('Context mandates a warning for this action')
        confirm = console.input(
            '[yellow]' +
            f'You are working on context "{config.active_context.name}". ' +
            'This action can be fatal. Continue? [ Y/n ] [/yellow]')
        if confirm.lower().strip() != 'y' and confirm.strip() != '':
            return

    logger.debug('Creating MyData object')
    data = get_global_data_object()
    data.configure(db_connection_str=config.active_context.db_string,
                   database_args={'echo': echo_sql})

    if drop_tables or create_data:
        logger.warning('All current data in the database will be lost!')

    logger.debug('Creating tables')
    data.create_db_tables(drop_tables=drop_tables)
    console.print('Created tables')

    if create_data:
        logger.debug('Creating test data')
        data.create_init_data()
        console.print('Created testdata')
