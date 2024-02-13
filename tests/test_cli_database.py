"""Tests to test the `database` subcommand for the tool."""
import pytest
from my_data.my_data import MyData
from rich.console import Console
from typer.testing import CliRunner

from my_multitool.__main__ import app
from my_multitool.globals import config

runner = CliRunner(echo_stdin=True)


def test_database_creation(
    data_object: MyData  # pylint: disable=unused-argument
) -> None:
    """Test the creation of the database.

    Args:
        data_object: fixture for the data object.
    """
    result = runner.invoke(app, ['database', 'create'])
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Created tables'


@pytest.mark.parametrize('answer', [
    'Y', 'y', '', ' Y ', ' y ', '     '
])
def test_database_creation_with_warning_confirm(
    data_object: MyData,  # pylint: disable=unused-argument
    answer: str
) -> None:
    """Test the creation of the database with a warning and a confirmation.

    Args:
        data_object: fixture for the data object.
        answer: the answer to give to the continue question.
    """
    def replacement_input(*args, **kwargs):  # pylint: disable=unused-argument
        return answer

    Console.input = replacement_input  # type:ignore

    config.active_context.warning = True
    result = runner.invoke(app, ['database', 'create'])
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Created tables'


@pytest.mark.parametrize('answer', [
    'N', 'n', 'x'
])
def test_database_creation_with_warning_not_confirm(
    data_object: MyData,  # pylint: disable=unused-argument
    answer: str
) -> None:
    """Test the creation of the database with a warning and not a confirmation.

    Args:
        data_object: fixture for the data object.
        answer: the answer to give to the continue question.
    """
    def replacement_input(*args, **kwargs):  # pylint: disable=unused-argument
        return answer

    Console.input = replacement_input  # type:ignore

    config.active_context.warning = True
    result = runner.invoke(app, ['database', 'create'])
    assert result.exit_code == 1
    assert result.stdout.strip() == ''


def test_database_creation_with_drop_tables(
    data_object: MyData  # pylint: disable=unused-argument
) -> None:
    """Test the creation of the database while dropping tables.

    Args:
        data_object: fixture for the data object.
    """
    result = runner.invoke(app, ['database', 'create', '--drop-tables'])
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Created tables'
