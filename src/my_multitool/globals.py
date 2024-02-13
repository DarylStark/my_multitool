"""Globals for the package.

Contains the global objects for the package.
"""
from typing import Optional, Any

from my_data.my_data import MyData

from .config import ConfigManager

config = ConfigManager()


def get_my_data_object_for_context(
        context_name: Optional[str] = None,
        db_args: Optional[dict[str, Any]] = None) -> MyData:
    """Get a configured MyData object for a specific context.

    Returns a MyData object with the correct configuration for the given
    context.

    Args:
        context_name: the name of the context to use. If not given, the active
            context will be used.
        db_args: additional arguments for the database connection.

    Returns:
        A MyData object.
    """
    if not context_name:
        context_name = config.active_context.name

    data = MyData()
    context = config.contexts[context_name]

    data.configure(
        db_connection_str=context.db_string,
        database_args=db_args,
        service_username=context.service_user,
        service_password=context.service_pass)

    return data
