"""The `users` portion of the CLI app.

Exposes the `users` commands for the CLI app.
"""
from getpass import getpass
from logging import getLogger

import typer
from my_data.exceptions import UnknownUserAccountException  # type:ignore
from my_model.user_scoped_models import User  # type:ignore

from .exceptions import GenericCLIException
from .globals import config, get_global_data_object
from .style import get_table, ConsoleFactory

app = typer.Typer(no_args_is_help=True)


@app.command(name='list')
def retrieve() -> None:
    """List users in the database.

    Lists all users in the database. It needs a Service Account and a Root
    account in order to do this. The service account should contain a password,
    the root account doesn't need this since the service account can just
    retrieve it.

    Raises:
        GenericCLIException: when no Service user or password is set in the
            active context.
    """
    logger = getLogger('users-list')
    console = ConsoleFactory.get_console()
    logger.info('Using config "%s"', config.active_context.name)

    logger.debug('Creating MyData object')
    data = get_global_data_object()

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
        try:
            user = context.get_user_account_by_username(
                config.active_context.root_user)
        except UnknownUserAccountException as exc:
            raise GenericCLIException(
                f'Unknown root user: "{config.active_context.root_user}"') \
                from exc

    if user:
        with data.get_context(user=user) as context:
            users = context.users.retrieve()
            table = get_table()
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


@app.command()
def set_password(username: str) -> None:
    """Set the password for a specific user.

    Resets the password for any user to a new password.

    Args:
        username: the username of the user to edit.

    Raises:
        GenericCLIException: when no Service user or password is set in the
            active context, or when the given passwords don't match.
    """
    logger = getLogger('users-set-password')
    logger.info('Using config "%s"', config.active_context.name)

    logger.debug('Creating MyData object')
    data = get_global_data_object()

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
        try:
            user = context.get_user_account_by_username(
                config.active_context.root_user)
        except UnknownUserAccountException as exc:
            raise GenericCLIException(
                f'Unknown root user: "{config.active_context.root_user}"') \
                from exc

    if user:
        new_password = getpass('Password: ')
        if len(new_password) == 0:
            raise GenericCLIException('Password too short')

        new_password_repeat = getpass('Repeat: ')
        if new_password != new_password_repeat:
            raise GenericCLIException('Passwords do not match')

        with data.get_context(user=user) as context:
            users_accounts = context.users.retrieve(User.username == username)
            if len(users_accounts) != 1:
                raise GenericCLIException(
                    f'User "{username}" not found.')
            users_accounts[0].set_password(new_password)
            context.users.update(users_accounts)
