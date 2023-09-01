"""The `contexts` portion of the CLI app.

Exposes the `contexts` commands for the CLI app. Contexts are a way to use this
tool with multiple deployments of the app. You can for instance create a
context for the development database, test database and production database.
Within the CLI, you can configure these contexts and active the one that is
appropiate for the work you have to do.
"""

import typer
from rich.console import Console

from .config import ContextModel
from .exceptions import GenericCLIException
from .globals import config
from .style import table_factory

app = typer.Typer(no_args_is_help=True)


@app.command(name='list')
def lst() -> None:
    """List configured contexts.

    Lists all configured contexts.

    Raises:
        GenericCLIException: when no contexts exists.
    """
    console = Console()
    contexts = config.contexts
    table = table_factory()
    table.add_column('*')
    table.add_column('Name')
    table.add_column('Database string')

    for name, context in contexts.items():
        active = ''
        if config.config:
            if config.config.active_context == name:
                active = '*'
        table.add_row(active, f'{name}', context.db_string)
    console.print(table)


@app.command(name='create')
def create(name: str, db_string: str) -> None:
    """Create a context.

    Creates a Context to use with the CLI app.

    Args:
        name: the name of the context.
        db_string: the string for the database connection.

    Raises:
        GenericCLIException: when there is already a context with this name.
    """
    console = Console()
    contexts = config.contexts
    if name in contexts.keys():
        raise GenericCLIException(
            f'Context with name "{name}" already exists')
    config.config.contexts.append(
        ContextModel(name=name, db_string=db_string))
    config.save()
    console.print(f'Context with name "{name}" is created')


@app.command(name='delete')
def delete(name: str) -> None:
    """Delete a context.

    Deletes a Context from the config.

    Args:
        name: the name of the context.

    Raises:
        GenericCLIException: when the given context doesn't exist.
    """
    console = Console()
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
    console = Console()
    contexts = config.contexts
    if context in contexts.keys() and config.config:
        config.config.active_context = context
        config.save()
        console.print(f'Now using "{context}"')
        return
    raise GenericCLIException(f'Context "{context}" is not configured.')
