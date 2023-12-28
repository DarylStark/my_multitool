import pathlib

import pytest
from my_data.my_data import MyData

from my_multitool.config import ConfigManager, ContextModel
from my_multitool.globals import config, get_global_data_object


@pytest.fixture
def config_object(tmp_path: pathlib.Path) -> ConfigManager:
    """Fixture for a global config object.

    Args:
        tmp_path: a temporary path created by PyTest.

    Returns:
        The created config object.
    """
    config.configure(f'{tmp_path}/.my_multitool_config.yaml')
    config.set_default_config()
    config.full_config.contexts.extend([
        ContextModel(name='context_01', db_string='sqlite:///:memory:/'),
        ContextModel(name='context_02',
                     db_string='sqlite:///:memory:/', warning=True),
        ContextModel(name='context_03', db_string='sqlite:///:memory:/'),
        ContextModel(name='context_04', db_string='sqlite:///:memory:/'),
        ContextModel(name='context_05', db_string='sqlite:///:memory:/')]
    )
    config.save()
    return config


@pytest.fixture
def data_object(config_object: ConfigManager) -> MyData:
    """Fixture for a global data object.

    Args:
        config_object: the fixture for the config object. We don't really use
            this, we just need it to make sure the correct configuration is
            created.

    Returns:
        The created MyData object.
    """
    return get_global_data_object()
