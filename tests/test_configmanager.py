"""Tests to test the `config` subcommand for the tool."""

import os

import pytest
from my_multitool.config import ConfigManager
from my_multitool.exceptions import (
    ConfigFileNotFoundError,
    NoConfigToSaveError,
)


@pytest.mark.parametrize(
    'attribute, expected_value',
    [
        ('name', 'default'),
        ('db_string', 'sqlite:///:memory:'),
        ('warning', False),
        ('service_user', 'service.user'),
        ('service_pass', 'service_password'),
        ('root_user', None),
    ],
)
def test_config_manager_default_config_default_context(
    config_object: ConfigManager,
    attribute: str,
    expected_value: str | bool | None,
) -> None:
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
    config_object.active_context.db_string = (
        'mysql+pymysql://username:password@sql.cloud.nl/database'
    )
    assert (
        config_object.active_context.db_string_with_masked_pwd
        == 'mysql+pymysql://username:***@sql.cloud.nl/database'
    )


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
    config_object.yaml_file = ''
    with pytest.raises(ConfigFileNotFoundError):
        config_object.load()


def test_loading_config_after_removing_the_file(
    config_object: ConfigManager,
) -> None:
    """Check if we get an error when the error file is removed.

    Args:
        config_object: fixture for the config object.
    """
    file = config_object.yaml_file
    os.remove(file)
    with pytest.raises(ConfigFileNotFoundError):
        config_object.load()


def test_saving_config_without_a_config(config_object: ConfigManager) -> None:
    """Save the config without a config.

    Args:
        config_object: fixture for the config object.
    """
    config_object.config = None  # type:ignore
    with pytest.raises(NoConfigToSaveError):
        config_object.save()


def test_saving_config_without_a_yaml_file(
    config_object: ConfigManager,
) -> None:
    """Save the config without a YAML file.

    Args:
        config_object: fixture for the config object.
    """
    config_object.yaml_file = ''
    with pytest.raises(NoConfigToSaveError):
        config_object.save()


def test_retrieving_full_config(config_object: ConfigManager) -> None:
    """Check if the retrieved full_config is correct.

    Args:
        config_object: fixture for the config object.
    """
    assert config_object.full_config is config_object.config


def test_retrieving_active_context(config_object: ConfigManager) -> None:
    """Check if the retrieved active_context is correct.

    Args:
        config_object: fixture for the config object.
    """
    assert config_object.active_context is config_object.active_context
