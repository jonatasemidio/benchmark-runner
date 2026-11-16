
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

    def run(self, cmd: str, is_check: bool = True, background: bool = False):
        """
        This method run shell commands
        :param background: run ssh in background
        :param cmd:
        :param is_check: run check command
        :return:
        """
        try:
            if background:
                return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                timeout=self.timeout,
            )
            output = result.stdout.removesuffix('\n')
            if is_check and result.returncode != 0:
                logger.error(f'subprocess Status : FAIL: {result.returncode} {output}')
                raise SSHSubprocessError()
            return output
        except Exception as err:
            raise err
