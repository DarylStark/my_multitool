"""The `contexts` portion of the CLI app.

Exposes the `contexts` commands for the CLI app. Contexts are a way to use this
tool with multiple deployments of the app. You can for instance create a
context for the development database, test database and production database.
Within the CLI, you can configure these contexts and active the one that is
appropiate for the work you have to do.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich import box
from .globals import config
from .exceptions import GenericCLIException

app = typer.Typer(no_args_is_help=True)


@app.command(name='list')
def lst() -> None:
    """List configured contexts.

    Lists all configured contexts.

    Raises:
        GenericCLIException: when no contexts exists
    """
    console = Console()
    contexts = config.contexts
    if contexts:
        table = Table(box=box.SIMPLE)
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
    else:
        raise GenericCLIException('No contexts set')


@app.command(name='create')
def create(name: str) -> None:
    """Create a context.

    Creates a Context to use with the CLI app.
    """


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
    if contexts:
        if context in contexts.keys() and config.config:
            config.config.active_context = context
            config.save()
            console.print(f'Now using "{context}"')
            return
    raise GenericCLIException(f'Context "{context}" is not configured.')
