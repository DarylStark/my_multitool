"""Configuration for PyTest."""
# pylint: disable=redefined-outer-name
import os

import pytest
from my_data.my_data import MyData
from my_data.my_data_table_creator import MyDataTableCreator
from my_data.data_loader import DataLoader, JSONDataSource

from my_multitool.config import ConfigManager, ContextModel
from my_multitool.globals import config, get_my_data_object_for_context


def test_filename() -> str:
    """Return the filename of the test data file.

    Returns:
        The filename of the test data file.
    """
    return os.path.join(os.path.dirname(__file__), 'test_data.json')


@pytest.fixture
def config_object(tmp_path_factory: pytest.TempPathFactory) -> ConfigManager:
    """Fixture for a global config object.

    Args:
        tmp_path_factory: a temporary path factory.

    Returns:
        The created config object.
    """
    tmp_path = tmp_path_factory.mktemp('my_multitool')
    config.configure(f'{tmp_path}/.my_multitool_config.yaml')
    config.set_default_config()
    config.contexts['default'].service_user = 'service.user'
    config.contexts['default'].service_pass = 'service_password'
    config.full_config.contexts.extend([
        ContextModel(name='context_01',
                     db_string='sqlite:///:memory:/',
                     service_user='service.user',
                     service_pass='service_password'),
        ContextModel(name='context_02',
                     db_string='sqlite:///:memory:/',
                     warning=True,
                     service_user='service.user',
                     service_pass='service_password'),
        ContextModel(name='context_03',
                     db_string='sqlite:///:memory:/',
                     service_user='service.user',
                     service_pass='service_password'),
        ContextModel(name='context_04',
                     db_string='sqlite:///:memory:/',
                     service_user='service.user',
                     service_pass='service_password'),
        ContextModel(name='context_05',
                     db_string='sqlite:///:memory:/',
                     service_user='service.user',
                     service_pass='service_password')]
    )
    config.save()
    return config


@pytest.fixture
def data_object(
    config_object: ConfigManager  # pylint: disable=unused-argument
) -> MyData:
    """Fixture for a global data object.

    Args:
        config_object: the fixture for the config object. We don't really use
            this, we just need it to make sure the correct configuration is
            created.

    Returns:
        The created MyData object.
    """
    return get_my_data_object_for_context(db_args={'echo': True})


@pytest.fixture
def data_object_with_tables(
        data_object: MyData) -> MyData:
    """Fixture for a global data object with tables.

    Args:
        data_object: a created data object with a database engine.

    Returns:
        The created MyData object.
    """
    creator = MyDataTableCreator(my_data_object=data_object)
    creator.create_db_tables()
    return data_object


@pytest.fixture
def data_object_with_database(
        data_object_with_tables: MyData) -> MyData:
    """Fixture for a global data object with a configured database.

    Args:
        data_object_with_tables: a created data object with database tables.

    Returns:
        The created MyData object.
    """
    # Create testdata
    loader = DataLoader(
        my_data_object=data_object_with_tables,
        data_source=JSONDataSource(
            test_filename()))
    loader.load()

    return data_object_with_tables


@pytest.fixture
def data_object_with_database_with_svc_user(
        data_object_with_database: MyData) -> MyData:
    """Fixture for a data object with a configured database and a svc user.

    Args:
        data_object_with_database: a data object with a configured database.

    Returns:
        The created MyData object.
    """
    config.active_context.service_user = 'service.user'
    config.active_context.service_pass = 'service_password'
    return data_object_with_database


@pytest.fixture
def data_object_with_database_with_root_user(  # pylint: disable=W0621
        data_object_with_database_with_svc_user: MyData) -> MyData:
    """Fixture for a data object with a configured database.

    Args:
        data_object_with_database_with_svc_user: a data object with a
            configured database and a service user.

    Returns:
        The created MyData object.
    """
    config.active_context.root_user = 'root'
    return data_object_with_database_with_svc_user


@pytest.fixture
def data_object_with_database_with_wrong_root_user(
        data_object_with_database_with_svc_user: MyData) -> MyData:
    """Fixture for a global data object with a configured database.

    Args:
        data_object_with_database_with_svc_user: a data object with a
            configured database, a service user and a wrong root user.

    Returns:
        The created MyData object.
    """
    config.active_context.root_user = 'wrong_root'
    return data_object_with_database_with_svc_user
