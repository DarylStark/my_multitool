"""The `database` portion of the CLI app.

Exposes the `database` commands for the CLI app.
"""
import typer

app = typer.Typer(no_args_is_help=True)


@app.command(name='create')
def create() -> None:
    """Create the database schema.

    Creates the database schema for the currently activated context.
    """
