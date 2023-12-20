"""Module to test the `version` command of the CLI script.

Test the `version` command of the script.
"""

from typer.testing import CliRunner
from my_multitool.__main__ import app
from my_multitool import __version__ as mymt_version
import re

runner = CliRunner(echo_stdin=True)


def test_version() -> None:
    """Run the `version` subcommand of the script.

    Tests if we get the correct version back.
    """
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert len(re.findall(
        f'^\s*My Multitool\s+{mymt_version}\s+$',
        result.output,
        re.MULTILINE)) == 1
