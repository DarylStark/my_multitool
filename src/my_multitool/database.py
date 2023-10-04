"""The `database` portion of the CLI app.

Exposes the `database` commands for the CLI app.
"""
from logging import getLogger

import typer
from my_data.my_data import MyData  # type:ignore

from .globals import config

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
    logger.info('Using config "%s"', config.active_context.name)

    logger.debug('Creating MyData object')
    data = MyData()
    data.configure(db_connection_str=config.active_context.db_string,
                   database_args={'echo': echo_sql})

    if drop_tables or create_data:
        logger.warning('All current data in the database will be lost!')

    logger.debug('Creating tables')
    data.create_db_tables(drop_tables=drop_tables)

    if create_data:
        logger.debug('Creating test data')
        data.create_init_data()
