
from my_data.my_data import MyData
import pytest
from typer.testing import CliRunner

from my_multitool.__main__ import app
from my_multitool.exceptions import GenericCLIException

runner = CliRunner(echo_stdin=True)


def test_users_retrieve_without_a_service_user(
        data_object_with_database: MyData) -> None:
    """Test if we get an error when retrieving without a service user.

    Args:
        data_object_with_database: a data object with a configured database.
    """
    result = runner.invoke(app, ['users', 'list'])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


def test_users_retrieve_without_a_root_user(
        data_object_with_database_with_svc_user: MyData) -> None:
    """Test if we get an error when retrieving without a service user.

    Args:
        data_object_with_database_with_svc_user: a data object with a
            configured database and a service user.
    """
    result = runner.invoke(app, ['users', 'list'])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


def test_users_retrieve(
        data_object_with_database_with_root_user: MyData,
        monkeypatch) -> None:
    """Test if we can retrieve users.

    Args:
        data_object_with_database_with_root_user: a data object with a
            configured database, a service user and a root user.
    """
    # Mocking the `get_global_data_object` function makes sure we always get
    # the same data object.
    monkeypatch.setattr(
        'my_multitool.users.get_global_data_object',
        lambda: data_object_with_database_with_root_user)
    result = runner.invoke(app, ['users', 'list'])
    assert result.exit_code == 0


def test_user_set_password_without_a_service_user(
        data_object_with_database: MyData) -> None:
    """Test is we get an error when updating a password without a service user.

    Args:
        data_object_with_database: a data object with a configured database.
    """
    result = runner.invoke(app, ['users', 'set-password', 'user'])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


def test_user_set_password_without_a_root_user(
        data_object_with_database_with_svc_user: MyData) -> None:
    """Test is we get an error when updating a password without a root user.

    Args:
        data_object_with_database_with_svc_user: a data object with a
            configured database and a service user.
    """
    result = runner.invoke(app, ['users', 'set-password', 'user'])
    assert result.exit_code != 0
    assert isinstance(result.exception, GenericCLIException)


@pytest.mark.parametrize('password', [
    'testpw', 'TeStPW', 'my_test_pw', 'very long password',
    ' a password with a space in the beginning'
])
def test_users_set_password(
        data_object_with_database_with_root_user: MyData,
        monkeypatch,
        password) -> None:
    """Test if we can reset the password for users.

    Args:
        data_object_with_database_with_root_user: a data object with a
            configured database, a service user and a root user.
        monkeypatch: the mocker.
        password: the password to test.
    """
    def replacement_input(*args, **kwargs):
        return password

    # Mocking the `get_global_data_object` function makes sure we always get
    # the same data object.
    monkeypatch.setattr(
        'my_multitool.users.get_global_data_object',
        lambda: data_object_with_database_with_root_user)
    monkeypatch.setattr('getpass.getpass', replacement_input)

    result = runner.invoke(app, ['users', 'set-password', 'normal.user.1'])
    assert result.exit_code == 0

    with data_object_with_database_with_root_user.get_context_for_service_user(
            'service.user', 'service_password') as c:
        user_account = c.get_user_account_by_username('normal.user.1')
    assert user_account.verify_credentials('normal.user.1', password)


def test_users_set_password_empty_password(
        data_object_with_database_with_root_user: MyData,
        monkeypatch) -> None:
    """Test if we can reset the password for users.

    Args:
        data_object_with_database_with_root_user: a data object with a
            configured database, a service user and a root user.
        monkeypatch: the mocker.
    """
    def replacement_input(*args, **kwargs):
        return ''

    # Mocking the `get_global_data_object` function makes sure we always get
    # the same data object.
    monkeypatch.setattr(
        'my_multitool.users.get_global_data_object',
        lambda: data_object_with_database_with_root_user)
    monkeypatch.setattr('getpass.getpass', replacement_input)
    result = runner.invoke(app, ['users', 'set-password', 'normal.user.1'])
    assert result.exit_code == 1
    assert isinstance(result.exception, GenericCLIException)


def test_users_set_password_inconsistent_passwords(
        data_object_with_database_with_root_user: MyData,
        monkeypatch) -> None:
    """Test if we can reset the password for users.

    Args:
        data_object_with_database_with_root_user: a data object with a
            configured database, a service user and a root user.
        monkeypatch: the mocker.
    """
    passwords = ['test', 'test1']

    def replacement_input(*args, **kwargs):
        password = passwords[0]
        passwords.pop(0)
        return password

    # Mocking the `get_global_data_object` function makes sure we always get
    # the same data object.
    monkeypatch.setattr(
        'my_multitool.users.get_global_data_object',
        lambda: data_object_with_database_with_root_user)
    monkeypatch.setattr('getpass.getpass', replacement_input)
    result = runner.invoke(app, ['users', 'set-password', 'normal.user.1'])
    assert result.exit_code == 1
    assert isinstance(result.exception, GenericCLIException)
