"""Globals for the package.

Contains the global objects for the package.
"""

from my_data.my_data import MyData  # type:ignore
from .config import ConfigManager

config = ConfigManager()


def get_global_data_object() -> MyData:
    """Get a configured MyData object.

    Returns a MyData object with the correct configuration for the active
    context.

    Returns:
        A MyData object.
    """
    data = MyData()
    data.configure(db_connection_str=config.active_context.db_string)
    return data
