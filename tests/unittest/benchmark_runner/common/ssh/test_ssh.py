
from benchmark_runner.common.ssh.ssh import SSH
from benchmark_runner.common.ssh.ssh_exceptions import SSHSubprocessError
from pytest import raises
from subprocess import DEVNULL
from subprocess import Popen


def test_run_cmd():
    """
    This method test run ssh cmd
    :return:
    """
    ssh = SSH()
    output = ssh.run(cmd='ls')
    assert output
    assert isinstance(output, str)


def test_run_consistent_str_output_across_is_check():
    ssh = SSH()
    unchecked = ssh.run("printf 'ready\\n'", is_check=False)
    checked = ssh.run("printf 'ready\\n'", is_check=True)
    assert isinstance(unchecked, str)
    assert isinstance(checked, str)
    assert checked == unchecked == 'ready'


def test_run_nonzero_exit_handling():
    ssh = SSH()
    unchecked = ssh.run("sh -c 'printf fail-msg >&2; exit 3'", is_check=False)
    assert unchecked == 'fail-msg'
    with raises(SSHSubprocessError):
        ssh.run("sh -c 'printf fail-msg >&2; exit 3'", is_check=True)


def test_run_universal_newlines_and_stderr_kwargs():
    ssh = SSH()
    raw = ssh.run("printf 'binary'", is_check=True, universal_newlines=False)
    assert raw == b'binary'
    quiet = ssh.run("sh -c 'printf out-only; printf err-only >&2'", is_check=True, stderr=DEVNULL)
    assert quiet == 'out-only'
    proc = ssh.run("printf 'bg'", background=True)
    try:
        assert isinstance(proc, Popen)
        stdout_data, _ = proc.communicate(timeout=5)
        assert 'bg' in stdout_data
    finally:
        proc.wait(timeout=5)
