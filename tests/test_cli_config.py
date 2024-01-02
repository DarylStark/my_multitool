"""Module to test the `config contexts` command of the CLI script.

Test the `config contexts` command of the script.
"""

import logging
import re

import pytest
from typer.testing import CliRunner

from my_multitool.__main__ import app  # type:ignore
from my_multitool.config import ConfigManager  # type:ignore
from my_multitool.exceptions import GenericCLIException  # type:ignore

runner = CliRunner(echo_stdin=True)


def test_context_list(config_object: ConfigManager) -> None:
    """Run the `config contexts list` subcommand of the script.

    Test is we can retrieve all contexts using the `config context list`
    command.

    Args:
        config_object: fixture for the config object.
    """
    result = runner.invoke(app, ['config', 'contexts', 'list'])
    assert result.exit_code == 0
    for name, context in config_object.contexts.items():
        assert len(re.findall(
            rf'{name}\s+{context.db_string}', result.stdout)) == 1


@pytest.mark.parametrize(
    'name, db_string, warning, service_user, service_pass, root_user', [
        ('test1', 'sqlite:///test.db', None, None, None, None),
        ('test2', 'sqlite:///test.db', True, None, None, None),
        ('test3', 'sqlite:///test.db', False, None, None, None),
        ('test4', 'sqlite:///test.db', None, 'svc_user', 'svc_pass', None),
        ('test5', 'sqlite:///test.db', None, None, None, 'root'),
    ])
def test_context_creation(
    config_object: ConfigManager,
    name: str,
    db_string: str,
    warning: bool | None,
    service_user: str | None,
    service_pass: str | None,
    root_user: str | None
) -> None:
    """Run the `config contexts create` subcommand of the script.

    Check if the context is created afterwards with the correct values.

    Args:
        config_object: fixture for the config object.
        name: the name of the context.
        db_string: the db string for the context.
        warning: the warning-flag for the context.
        service_user: the service user for the context.
        service_pass: the service password for the context.
        root_user: the root user for the context.
    """
    args = ['config',
            'contexts',
            'create',
            name,
            db_string]

    if warning is not None:
        if warning is True:
            args.append('--warning')
        else:
            args.append('--no-warning')

    if service_user:
        args.extend(['--service-user', service_user])
    if service_pass:
        args.extend(['--service-pass', service_pass])
    if root_user:
        args.extend(['--root-user', root_user])

    result = runner.invoke(app, args)

    if not warning:
        warning = False

    assert result.exit_code == 0
    assert config_object.contexts[name].db_string == db_string
    assert config_object.contexts[name].warning == warning
    assert config_object.contexts[name].service_user == service_user
    assert config_object.contexts[name].service_pass == service_pass
    assert config_object.contexts[name].root_user == root_user


def test_context_creation_existing_context(
        config_object: ConfigManager  # pylint: disable=unused-argument
) -> None:
    """Test adding duplicate contexts.

    Create a context that already exists and check if we get an error.

    Args:
        config_object: fixture for the config object.
    """
    result = runner.invoke(app, [
        'config',
        'contexts',
        'create',
        'default',
        'sqlite:///:memory:/'
    ])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


@pytest.mark.parametrize('context_name', [
    'context_01',
    'context_02',
    'context_03',
    'context_04',
    'context_05'
])
def test_context_use(config_object: ConfigManager, context_name: str) -> None:
    """Test is we can change the active context.

    Args:
        config_object: fixture for the config object.
        context_name: the context name to test.
    """
    result = runner.invoke(app, [
        'config',
        'contexts',
        'use',
        context_name
    ])
    assert result.exit_code == 0
    assert config_object.active_context.name == context_name
    assert config_object.full_config.active_context == context_name


def test_context_use_wrong_context(
        config_object: ConfigManager  # pylint: disable=unused-argument
) -> None:
    """Test is we get an error when chaning to a non existing context.

    Args:
        config_object: fixture for the config object.
    """
    result = runner.invoke(app, [
        'config',
        'contexts',
        'use',
        'non_existing_context'
    ])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


@pytest.mark.parametrize('context_name', [
    'context_01',
    'context_02',
    'context_03',
    'context_04',
    'context_05'
])
def test_context_delete(
        config_object: ConfigManager, context_name: str) -> None:
    """Test is we can delete contexts.

    Args:
        config_object: fixture for the config object.
        context_name: the context name to test.
    """
    result = runner.invoke(app, [
        'config',
        'contexts',
        'delete',
        context_name
    ])
    assert result.exit_code == 0
    assert context_name not in config_object.contexts.keys()


def test_context_delete_active_context(config_object: ConfigManager) -> None:
    """Test is we get an error when deleting the active context.

    Args:
        config_object: fixture for the config object.
    """
    result = runner.invoke(app, [
        'config',
        'contexts',
        'delete',
        config_object.full_config.active_context
    ])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


@pytest.mark.parametrize(
    'name, db_string, warning, service_user, ' +
    'service_pass, root_user, new_name', [
        ('context_01', 'sqlite:///test.db', None, None, None, None, None),
        ('context_02', 'sqlite:///test.db', True, None, None, None, None),
        ('context_03', 'sqlite:///test.db', False, None, None, None, None),
        ('context_04', 'sqlite:///test.db', None,
         'svc_user', 'svc_pass', None, None),
        ('context_05', 'sqlite:///test.db', None, None, None, 'root', None),
        ('context_01', 'sqlite:///test.db', None,
         None, None, 'root', 'context_01_new_name'),
    ])
def test_context_set(  # pylint: disable=too-many-branches
    config_object: ConfigManager,  # pylint: disable=unused-argument
    name: str,
    db_string: str,
    warning: bool | None,
    service_user: str | None,
    service_pass: str | None,
    root_user: str | None,
    new_name: str | None
) -> None:
    """Run the `config contexts set` subcommand of the script.

    Check if the context is updated after running the `set` subcommand.

    Args:
        config_object: fixture for the config object.
        name: the name of the context.
        db_string: the db string for the context.
        warning: the warning-flag for the context.
        service_user: the service user for the context.
        service_pass: the service password for the context.
        root_user: the root user for the context.
        new_name: the new name for the context.
    """
    args = ['config',
            'contexts',
            'set',
            name]

    if warning is not None:
        if warning is True:
            args.append('--warning')
        else:
            args.append('--no-warning')

    if db_string:
        args.extend(['--db-string', db_string])
    if service_user:
        args.extend(['--service-user', service_user])
    if service_pass:
        args.extend(['--service-pass', service_pass])
    if root_user:
        args.extend(['--root-user', root_user])
    if new_name:
        args.extend(['--new-name', new_name])

    result = runner.invoke(app, args)

    assert result.exit_code == 0
    if new_name:
        name = new_name
        assert config_object.contexts[name].name == new_name
    if db_string:
        assert config_object.contexts[name].db_string == db_string
    if warning is not None:
        assert config_object.contexts[name].warning == warning
    if service_pass:
        assert config_object.contexts[name].service_user == service_user
    if service_pass:
        assert config_object.contexts[name].service_pass == service_pass
    if root_user:
        assert config_object.contexts[name].root_user == root_user


def test_context_rename_active_context(config_object: ConfigManager) -> None:
    """Rename a active context.

    Check if the `active_context` property gets updates.

    Args:
        config_object: fixture for the config object.
    """
    result = runner.invoke(app, [
        'config', 'contexts', 'set', config_object.full_config.active_context,
        '--new-name', 'new_name_for_context'
    ])
    assert result.exit_code == 0
    assert config_object.full_config.active_context == 'new_name_for_context'


def test_context_updating_non_existing_context(
        config_object: ConfigManager  # pylint: disable=unused-argument
) -> None:
    """Edit a non-existing context to see if we get an error.

    Args:
        config_object: fixture for the config object.
    """
    result = runner.invoke(app, [
        'config',
        'contexts',
        'set',
        'non_existing_context'
    ])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


def test_context_deleting_non_existing_context(
        config_object: ConfigManager  # pylint: disable=unused-argument
) -> None:
    """Delete a non-existing context to see if we get an error.

    Args:
        config_object: fixture for the config object.
    """
    result = runner.invoke(app, [
        'config',
        'contexts',
        'delete',
        'non_existing_context'
    ])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


@pytest.mark.parametrize('level_string, level_value', [
    ('debug', logging.DEBUG),
    ('info', logging.INFO),
    ('warning', logging.WARNING),
    ('error', logging.ERROR),
    ('fatal', logging.FATAL)
])
def test_set_logging_level(config_object: ConfigManager,
                           level_string: str, level_value: int) -> None:
    """Set a logging level.

    Set the logging level and check if it is updated.

    Args:
        config_object: fixture for the config object.
        level_string: the name for the level.
        level_value: the integer for the level.
    """
    result = runner.invoke(app, [
        'config',
        'set-logging-level',
        level_string
    ])
    assert result.exit_code == 0
    assert config_object.full_config.logging_level == level_value
