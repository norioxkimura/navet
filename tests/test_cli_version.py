
from click.testing import CliRunner
from navet import cli

def test_cli_navet_version():
    runner = CliRunner()
    result = runner.invoke(cli.navet, [ 'version' ])
    assert result.exit_code == 0
    assert result.output == 'navet 0.1\n'

