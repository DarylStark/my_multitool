"""The `contexts` portion of the CLI app.

Exposes the `contexts` commands for the CLI app. Contexts are a way to use this
tool with multiple deployments of the app. You can for instance create a
context for the development database, test database and production database.
Within the CLI, you can configure these contexts and active the one that is
appropiate for the work you have to do.
"""

import typer

from .config import ContextModel
from .exceptions import GenericCLIException
from .globals import config
from .style import get_table, ConsoleFactory

app = typer.Typer(no_args_is_help=True)


@app.command(name='create')
def create(
    name: str,
    db_string: str,
    warning: bool = False,
    service_user: str | None = None,
    service_pass: str | None = None,
    root_user: str | None = None,
) -> None:
    """Create a context.

    Creates a Context to use with the CLI app.

    Args:
        name: the name of the context.
        db_string: the string for the database connection.
        warning: if the context should generate a warning before running
            anything.
        service_user: the service user to use when connecting to this instance.
        service_pass: the password for the service user.
        root_user: the username of a root user to use when working with users.

    Raises:
        GenericCLIException: when there is already a context with this name.
    """
    console = ConsoleFactory.get_console()
    contexts = config.contexts
    if name in contexts.keys():
        raise GenericCLIException(
            f'Context with name "{name}" already exists')
    config.config.contexts.append(
        ContextModel(
            name=name,
            db_string=db_string,
            warning=warning,
            service_user=service_user,
            service_pass=service_pass,
            root_user=root_user))
    config.save()
    console.print(f'Context with name "{name}" is created')


@app.command(name='list')
def retrieve() -> None:
    """List configured contexts.

    Lists all configured contexts.
    """
    console = ConsoleFactory.get_console()
    contexts = config.contexts
    table = get_table()
    table.add_column('*')
    table.add_column('Name')
    table.add_column('Database string')
    table.add_column('Warning')
    table.add_column('Service user')
    table.add_column('Root user')

    for name, context in contexts.items():
        active = ''
        warning = ''
        if config.config:
            if config.config.active_context == name:
                active = '*'
            warning = '*' if context.warning else ''
        table.add_row(active, f'{name}',
                      context.db_string_with_masked_pwd,
                      warning,
                      context.service_user,
                      context.root_user)
    console.print(table)


@app.command(name='set')
def update(name: str,
           new_name: str | None = None,
           db_string: str | None = None,
           warning: bool | None = None,
           service_user: str | None = None,
           service_pass: str | None = None,
           root_user: str | None = None,
           ) -> None:
    """Update a configured context.

    Updates a configured context.

    Args:
        name: the name of the context to update.
        new_name: a new name for the context.
        db_string: a new DB string for the context.
        warning: if the context should generate a warning before running
            anything.
        service_user: the service user to use when connecting to this instance.
        service_pass: the password for the service user.
        root_user: the username of a root user to use when working with users.

    Raises:
        GenericCLIException: when the given context doesn't exist.
    """
    console = ConsoleFactory.get_console()
    contexts = config.contexts
    selected_context = contexts.get(name)
    if selected_context:
        # Set the updated fields
        if new_name:
            selected_context.name = new_name
            if config.config.active_context == name:
                config.config.active_context = new_name
        if db_string:
            selected_context.db_string = db_string
        if warning is not None:
            selected_context.warning = warning
        if service_user is not None:
            selected_context.service_user = service_user
        if service_pass is not None:
            selected_context.service_pass = service_pass
        if root_user is not None:
            selected_context.root_user = root_user

        config.save()
        console.print(f'Context with name "{name}" is updated')
        return
    raise GenericCLIException(
        f'Context with name "{name}" does not exist')


@app.command(name='delete')
def delete(name: str) -> None:
    """Delete a context.

    Deletes a Context from the config.

    Args:
        name: the name of the context.

    Raises:
        GenericCLIException: when the given context doesn't exist or when the
            user tries to remove the context that is active.
    """
    if config.config.active_context == name:
        raise GenericCLIException('Cannot remove active context')

    console = ConsoleFactory.get_console()
    contexts = config.contexts
    if contexts.get(name):
        config.config.contexts = list(filter(
            lambda x: x.name != name,
            config.config.contexts))
        config.save()
        console.print(f'Context with name "{name}" is deleted')
        return
    raise GenericCLIException(
        f'Context with name "{name}" does not exist')


@app.command(name='use')
def use(context: str) -> None:
    """Use a context.

    Activates a context.

    Args:
        context: the context to activate.

    Raises:
        GenericCLIException: when the selected context does not exists.
    """
    console = ConsoleFactory.get_console()
    contexts = config.contexts
    if context in contexts.keys() and config.config:
        config.config.active_context = context
        config.save()
        console.print(f'Now using "{context}"')
        return
    raise GenericCLIException(f'Context "{context}" is not configured.')
