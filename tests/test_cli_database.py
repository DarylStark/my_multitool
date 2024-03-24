"""Tests to test the `database` subcommand for the tool."""

from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch
from my_data.my_data import MyData
from my_multitool.__main__ import app
from my_multitool.globals import config
from rich.console import Console
from typer.testing import CliRunner

runner = CliRunner(echo_stdin=True)


def test_database_creation(
    data_object: MyData,  # pylint: disable=unused-argument
) -> None:
    """Test the creation of the database.

    Args:
        data_object: fixture for the data object.
    """
    result = runner.invoke(app, ['database', 'create'])
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Created tables'


@pytest.mark.parametrize('answer', ['Y', 'y', '', ' Y ', ' y ', '     '])
def test_database_creation_with_warning_confirm(
    data_object: MyData,  # pylint: disable=unused-argument
    answer: str,
) -> None:
    """Test the creation of the database with a warning and a confirmation.

    Args:
        data_object: fixture for the data object.
        answer: the answer to give to the continue question.
    """

    def replacement_input(*args: list[Any], **kwargs: dict[Any, Any]) -> str:
        return answer

    Console.input = replacement_input  # type:ignore

    config.active_context.warning = True
    result = runner.invoke(app, ['database', 'create'])
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Created tables'


@pytest.mark.parametrize('answer', ['N', 'n', 'x'])
def test_database_creation_with_warning_not_confirm(
    data_object: MyData,  # pylint: disable=unused-argument
    answer: str,
) -> None:
    """Test the creation of the database with a warning and not a confirmation.

    Args:
        data_object: fixture for the data object.
        answer: the answer to give to the continue question.
    """

    def replacement_input(*args: list[Any], **kwargs: dict[Any, Any]) -> str:
        return answer

    Console.input = replacement_input  # type:ignore

    config.active_context.warning = True
    result = runner.invoke(app, ['database', 'create'])
    assert result.exit_code == 1
    assert result.stdout.strip() == ''


def test_database_creation_with_drop_tables(
    data_object: MyData,  # pylint: disable=unused-argument
) -> None:
    """Test the creation of the database while dropping tables.

    Args:
        data_object: fixture for the data object.
    """
    result = runner.invoke(app, ['database', 'create', '--drop-tables'])
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Created tables'


def test_database_import_json(
    data_object_with_tables: MyData, monkeypatch: MonkeyPatch
) -> None:
    """Test the import of a JSON file into the database.

    Args:
        data_object_with_tables: fixture for the data object.
        monkeypatch: a monkeypatch fixture.
    """

    def replacement_data(*args: list[Any], **kwargs: dict[Any, Any]) -> str:
        return data_object_with_tables

    monkeypatch.setattr(
        'my_multitool.cli_database.get_my_data_object_for_context',
        replacement_data,
    )

    result = runner.invoke(
        app, ['database', 'import-json', 'tests/test_data.json']
    )
    assert result.exit_code == 0
    assert result.stdout.strip() == 'Imported data'


def test_database_import_json_wrong_filename(
    data_object_with_tables: MyData, monkeypatch: MonkeyPatch
) -> None:
    """Test the import of a JSON file into the database with wrong filename.

    Args:
        data_object_with_tables: fixture for the data object.
        monkeypatch: a monkeypatch fixture.
    """

    def replacement_data(*args: list[Any], **kwargs: dict[Any, Any]) -> str:
        return data_object_with_tables

    monkeypatch.setattr(
        'my_multitool.cli_database.get_my_data_object_for_context',
        replacement_data,
    )

    result = runner.invoke(app, ['database', 'import-json', 'wrong-file.json'])
    assert result.exit_code == 1


def test_database_import_json_integrity_error(
    data_object_with_database: MyData, monkeypatch: MonkeyPatch
) -> None:
    """Test the import of a JSON file into the database with data.

    Args:
        data_object_with_database: fixture for the data object.
        monkeypatch: a monkeypatch fixture.
    """

    def replacement_data(*args: list[Any], **kwargs: dict[Any, Any]) -> str:
        return data_object_with_database

    monkeypatch.setattr(
        'my_multitool.cli_database.get_my_data_object_for_context',
        replacement_data,
    )

    result = runner.invoke(
        app, ['database', 'import-json', 'tests/test_data.json']
    )
    assert result.exit_code == 1
