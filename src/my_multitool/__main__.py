"""Main entry point for the CLI script.

This module contains the `main()` method that exposes the CLI arguments for the
script. The CLI argument groups are imported from other modules.
"""
import typer

from .database import app as database_app
from .contexts import app as contexts_app

def main() -> None:
    """Entry point for the CLI script.

    Defines the commands for the CLI script and makes sure the correct
    functions get called when running a specific CLI command.
    """
    app = typer.Typer(no_args_is_help=True)

    # Add subcommand's
    app.add_typer(database_app, name='database', help='Database management')
    app.add_typer(contexts_app, name='contexts', help='Context management')

    # Run the Typer app
    app()


if __name__ == '__main__':
    main()
