"""The `users` portion of the CLI app.

Exposes the `users` commands for the CLI app.
"""
from logging import getLogger

import typer
from my_data.my_data import MyData  # type:ignore
from rich.console import Console

from .exceptions import GenericCLIException

from .globals import config
from .style import table_factory

app = typer.Typer(no_args_is_help=True)


@app.command(name='list')
def retrieve() -> None:
    """List users in the database.

    Lists all users in the database. It needs a Service Account and a Root
    account in order to do this. The service account should contain a password,
    the root account doesn't need this since the service account can just
    retrieve it.
    """
    logger = getLogger('users-list')
    console = Console()
    logger.info('Using config "%s"', config.active_context.name)

    # TODO: duplicate code; move to function
    logger.debug('Creating MyData object')
    data = MyData()
    data.configure(db_connection_str=config.active_context.db_string)

    user = None
    if any((
        config.active_context.service_user is None,
        config.active_context.service_pass is None,
        config.active_context.root_user is None,
    )):
        raise GenericCLIException(
            'Service user credentials or root user not set in active context')

    with data.get_context_for_service_user(
            username=config.active_context.service_user,
            password=config.active_context.service_pass) as context:
        user = context.get_user_account_by_username(
            config.active_context.root_user)

    if user:
        with data.get_context(user=user) as context:
            users = context.users.retrieve()
            table = table_factory()
            table.add_column('#')
            table.add_column('Fullname')
            table.add_column('Username')
            table.add_column('Role')
            table.add_column('Second factor')

            for user in users:
                table.add_row(
                    str(user.id),
                    user.fullname,
                    user.username,
                    str(user.role),
                    'Yes' if user.second_factor else 'No')
            console.print(table)
