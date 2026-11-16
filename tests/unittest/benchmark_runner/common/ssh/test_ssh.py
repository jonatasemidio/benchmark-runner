
from benchmark_runner.common.ssh.ssh import SSH
from benchmark_runner.common.ssh.ssh_exceptions import SSHSubprocessError
import pytest


def test_run_cmd():
    """
    This method test run ssh cmd
    :return:
    """
    ssh = SSH()
    assert isinstance(ssh.run(cmd='ls'), str)


def test_run_checks_exit_code_by_default():
    ssh = SSH()
    with pytest.raises(SSHSubprocessError):
        ssh.run(cmd='exit 1')


def test_run_is_check_false_ignores_nonzero_exit():
    ssh = SSH()
    output = ssh.run(cmd='printf "warn\\n" >&2; exit 1', is_check=False)
    assert output == 'warn'
    assert isinstance(output, str)


def test_run_returns_identical_str_output_in_both_modes():
    ssh = SSH()
    checked = ssh.run(cmd='printf "line1\\nline2\\n"', is_check=True)
    unchecked = ssh.run(cmd='printf "line1\\nline2\\n"', is_check=False)
    assert checked == 'line1\nline2'
    assert checked == unchecked
    assert isinstance(checked, str)
    assert isinstance(unchecked, str)
