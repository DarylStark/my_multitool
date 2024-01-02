"""Module to test the `version` command of the CLI script.

Test the `version` command of the script.
"""

import re

from typer.testing import CliRunner

from my_multitool import __version__ as mymt_version  # type:ignore
from my_multitool.__main__ import app  # type:ignore

runner = CliRunner(echo_stdin=True)


def test_version() -> None:
    """Run the `version` subcommand of the script.

    Tests if we get the correct version back and if the returncode for the
    command is 0 (= no error).
    """
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert len(re.findall(
        r'^\s*My Multitool\s+' + mymt_version + r'\s+$',
        result.output,
        re.MULTILINE)) == 1
