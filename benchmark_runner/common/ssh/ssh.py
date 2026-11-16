
import subprocess
from benchmark_runner.common.logger.logger_time_stamp import logger
from benchmark_runner.common.ssh.ssh_exceptions import SSHSubprocessError
from benchmark_runner.main.environment_variables import environment_variables


class SSH:
    """
    This class run local SSH commands
    """
    def __init__(self):
        self.__environment_variables_dict = environment_variables.environment_variables_dict
        self.timeout = int(self.__environment_variables_dict.get('timeout', 300))

    def run(
        self,
        cmd: str,
        is_check: bool = False,
        background: bool = False,
        universal_newlines: bool = True,
        stderr=subprocess.STDOUT,
    ):
        """
        This method run shell commands
        :param cmd: command to execute
        :param is_check: check command exit status
        :param background: run ssh in background
        :param universal_newlines: decode command output as text
        :param stderr: stderr target passed to subprocess
        :return: command output (str by default, bytes when universal_newlines=False, or Popen when background=True)
        """
        try:
            if background:
                return subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=stderr,
                    universal_newlines=universal_newlines,
                )
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=stderr,
                shell=True,
                timeout=self.timeout,
                universal_newlines=universal_newlines,
                check=is_check,
            )
            output = result.stdout
            if isinstance(output, str) and output.endswith('\n'):
                output = output[:-1]
            return output
        except subprocess.CalledProcessError as err:
            logger.error(f'subprocess Status : FAIL: {err.returncode} {err.output}')
            raise SSHSubprocessError()
        except Exception as err:
            raise err
