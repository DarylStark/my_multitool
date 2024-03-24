"""Tests for the global style of the application."""

import pytest
from _pytest.monkeypatch import MonkeyPatch
from my_multitool.style import print_error


@pytest.mark.parametrize('message', ['testmessage', 'Something went wrong'])
@pytest.mark.parametrize(
    'prefix', ['error', 'ERROR', 'warning', 'WARNING', 'CRITICAL']
)
def test_print_error(
    message: str, prefix: str, monkeypatch: MonkeyPatch
) -> None:
    """Test the `print_error` function.

    Args:
        message: the message for the `print_error` function.
        prefix: the prefix for the `print_error` function.
        monkeypatch: the mocker.
    """

    def test_print_statement(
        obj: object,
        input_text: str,
    ) -> None:
        assert input_text == f'[red][b]{prefix}:[/b] {message}'

    monkeypatch.setattr('rich.console.Console.print', test_print_statement)
    print_error(message, prefix)
