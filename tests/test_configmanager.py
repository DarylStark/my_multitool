"""Tests to test the `config` subcommand for the tool."""

from logging import config
from threading import active_count
from my_multitool.config import ConfigManager
import pytest
import os

from my_multitool.exceptions import ConfigFileNotFoundException, ConfigFileNotValidException


@pytest.mark.parametrize('attribute, expected_value', [
    ('name', 'default'),
    ('db_string', 'sqlite:///:memory:'),
    ('warning', False),
    ('service_user', None),
    ('service_pass', None),
    ('root_user', None),
])
def test_config_manager_default_config_default_context(
        config_object: ConfigManager,
        attribute: str, expected_value: str | bool | None) -> None:
    """Test the defaults for the active context.

    Args:
        config_object: fixture for the config object.
        attribute: the attribute to test.
        expected_value: the value to check.
    """
    assert getattr(config_object.active_context, attribute) == expected_value


def test_masked_password(config_object: ConfigManager) -> None:
    """Set a db string with a password and check the masking.

    Args:
        config_object: fixture for the config object.
    """
    config_object.active_context.db_string = 'mysql+pymysql://username:password@sql.cloud.nl/database'
    assert config_object.active_context.db_string_with_masked_pwd == 'mysql+pymysql://username:***@sql.cloud.nl/database'


def test_loading_config_from_file(config_object: ConfigManager) -> None:
    """Test loading the configuration from file.

    Args:
        config_object: fixture for the config object.
    """
    config_object.active_context.name = 'test'
    config_object.full_config.active_context = 'test'
    config_object.save()
    config_object.load()
    assert config_object.active_context.name == 'test'
    assert config_object.full_config.active_context == 'test'


def test_loading_config_without_a_file(config_object: ConfigManager) -> None:
    """Check if we get an error when no YAML file is set.

    Args:
        config_object: fixture for the config object.
    """
    config_object.yaml_file = None
    with pytest.raises(ConfigFileNotFoundException):
        config_object.load()


def test_loading_config_after_removing_the_file(config_object: ConfigManager) -> None:
    """Check if we get an error when the error file is removed.

    Args:
        config_object: fixture for the config object.
    """
    file = config_object.yaml_file
    os.remove(file)
    with pytest.raises(ConfigFileNotFoundException):
        config_object.load()


def test_loading_a_incorrect_yaml_file(config_object: ConfigManager) -> None:
    """Check if we get an error when the file is incorrect.

    Args:
        config_object: fixture for the config object.
    """
    file = config_object.yaml_file
    with open(file, 'a', encoding='utf-8') as yaml_file:
        yaml_file.write('aaa')
    with pytest.raises(ConfigFileNotValidException):
        config_object.load()


@pytest.mark.xfail(reason='Test not implemented yet')
def test_loading_a_invalid_config_file(config_object: ConfigManager) -> None:
    """Write wrong values to the YAML file to see if loading fails.

    Args:
        config_object: fixture for the config object.
    """
    assert False
