"""The `users` portion of the CLI app.

Exposes the `users` commands for the CLI app.
"""

import getpass
from logging import getLogger

import typer
from my_data.exceptions import UnknownUserAccountError
from my_model import User

from .exceptions import GenericCLIError
from .globals import config, get_my_data_object_for_context
from .style import ConsoleFactory, get_table

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
    data = get_my_data_object_for_context()

    user = None
    if any(
        (
            config.active_context.service_user is None,
            config.active_context.service_pass is None,
            config.active_context.root_user is None,
        )
    ):
        raise GenericCLIError(
            'Service user credentials or root user not set in active context'
        )

    with data.get_context_for_service_user() as context:
        try:
            user = context.get_user_account_by_username(
                str(config.active_context.root_user)
            )
        except UnknownUserAccountError as exc:
            raise GenericCLIError(
                f'Unknown root user: "{config.active_context.root_user}"'
            ) from exc

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
                    'Yes' if user.second_factor else 'No',
                )
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
    data = get_my_data_object_for_context()

    user = None
    if any(
        (
            config.active_context.service_user is None,
            config.active_context.service_pass is None,
            config.active_context.root_user is None,
        )
    ):
        raise GenericCLIError(
            'Service user credentials or root user not set in active context'
        )

    with data.get_context_for_service_user() as context:
        try:
            user = context.get_user_account_by_username(
                str(config.active_context.root_user)
            )
        except UnknownUserAccountError as exc:
            raise GenericCLIError(
                f'Unknown root user: "{config.active_context.root_user}"'
            ) from exc

    if user:
        new_password = getpass.getpass('Password: ')
        if len(new_password) == 0:
            raise GenericCLIError('Password too short')

        new_password_repeat = getpass.getpass('Repeat: ')
        if new_password != new_password_repeat:
            raise GenericCLIError('Passwords do not match')

        with data.get_context(user=user) as context:
            users_accounts = context.users.retrieve(
                User.username  # type:ignore
                == username
            )
            if len(users_accounts) != 1:
                raise GenericCLIError(f'User "{username}" not found.')
            users_accounts[0].set_password(new_password)
            context.users.update(users_accounts)
