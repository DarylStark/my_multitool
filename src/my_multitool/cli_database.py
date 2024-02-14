"""The `database` portion of the CLI app.

Exposes the `database` commands for the CLI app.
"""
from logging import getLogger

import typer
from my_data.data_loader import DataLoader, JSONDataSource
from my_data.my_data_table_creator import MyDataTableCreator
from sqlalchemy.exc import IntegrityError

from my_multitool.exceptions import (GenericCLIException, SQLError,
                                     NoConfirmationException)

from .globals import config, get_my_data_object_for_context
from .style import ConsoleFactory

app = typer.Typer(no_args_is_help=True)


@app.command(name='create')
def create(echo_sql: bool = False,
           drop_tables: bool = False) -> None:
    """Create the database schema.

    Creates the database schema for the currently activated context.

    Args:
        echo_sql: if set to True, the SQL queries that are executed will be
            displayed. This can be usefull to see what is happening.
        drop_tables: if set to True, all tables will be dropped which will
            result in data loss.

    Raises:
        NoConfirmationException: when the user presses 'N' at the question if
            he wants to continue.
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
            raise NoConfirmationException

    logger.debug('Creating MyData object')
    data = get_my_data_object_for_context(
        context_name=None, db_args={'echo': echo_sql})

    if drop_tables:
        logger.warning('All current data in the database will be lost!')

    logger.debug('Creating tables')
    creator = MyDataTableCreator(my_data_object=data)
    creator.create_db_tables(drop_tables=drop_tables)
    console.print('Created tables')


@app.command(name='import-json')
def import_json(filename: str, echo_sql: bool = False) -> None:
    """Import data from a JSON file.

    Args:
        filename: the name of the file to import.
        echo_sql: if set to True, the SQL queries that are executed will be
            displayed. This can be usefull to see what is happening.

    Raises:
        GenericCLIException: when the file to import is not found.
        SQLError: when an SQL error occurs.
    """
    logger = getLogger('database-import-json')
    console = ConsoleFactory.get_console()

    logger.debug('Creating MyData object')
    data = get_my_data_object_for_context(
        context_name=None, db_args={'echo': echo_sql})
    data.create_engine()

    loader = DataLoader(
        my_data_object=data,
        data_source=JSONDataSource(filename))
    logger.info('Importing data from file "%s"', filename)

    try:
        loader.load()
    except FileNotFoundError as exception:
        raise GenericCLIException(
            f'File not found: {filename}') from exception
    except IntegrityError as exception:
        raise SQLError(','.join(exception.args)) from exception
    console.print('Imported data')
