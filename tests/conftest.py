import pathlib

import pytest
from my_data.my_data import MyData

from my_multitool.config import ConfigManager, ContextModel
from my_multitool.globals import config, get_global_data_object


@pytest.fixture
def config_object(tmp_path_factory: pytest.TempPathFactory) -> ConfigManager:
    """Fixture for a global config object.

    Args:
        tmp_path: a temporary path created by PyTest.

    Returns:
        The created config object.
    """
    tmp_path = tmp_path_factory.mktemp('my_multitool')
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


@pytest.fixture
def data_object_with_database(data_object: MyData) -> MyData:
    """Fixture for a global data object with a configured database.

    Args:
        data_object: a created data object with database tables and
            initialization data.

    Returns:
        The created MyData object.
    """
    data_object.create_db_tables()
    data_object.create_init_data()
    return data_object


@pytest.fixture
def data_object_with_database_with_svc_user(
        data_object_with_database: MyData) -> MyData:
    """Fixture for a global data object with a configured database and a svc
    user.

    Args:
        data_object_with_database: a data object with a configured database.

    Returns:
        The created MyData object.
    """
    config.active_context.service_user = 'service.user'
    config.active_context.service_pass = 'service_password'
    return data_object_with_database


@pytest.fixture
def data_object_with_database_with_root_user(
        data_object_with_database_with_svc_user: MyData) -> MyData:
    """Fixture for a global data object with a configured database, a svc user
    and a root user

    Args:
        data_object_with_database_with_svc_user: a data object with a
            configured database and a service user.

    Returns:
        The created MyData object.
    """
    config.active_context.root_user = 'root'
    return data_object_with_database_with_svc_user
