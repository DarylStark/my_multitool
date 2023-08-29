"""The `contexts` portion of the CLI app.

Exposes the `contexts` commands for the CLI app. Contexts are a way to use this
tool with multiple deployments of the app. You can for instance create a
context for the development database, test database and production database.
Within the CLI, you can configure these contexts and active the one that is
appropiate for the work you have to do.
"""

import typer

app = typer.Typer(no_args_is_help=True)


@app.command(name='list')
def lst() -> None:
    """List configured contexts.

    Lists all configured contexts.
    """

@app.command(name='create')
def create() -> None:
    """Create a context.

    Creates a Context to use with the CLI app.
    """

@app.command(name='use')
def use() -> None:
    """Use a context.

    Activates a context.
    """