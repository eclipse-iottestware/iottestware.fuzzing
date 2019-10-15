# ********************************************************************************
# Copyright (c) 2019 Alexander Kaiser
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#   Alexander Kaiser - initial API and implementation
# ********************************************************************************

import paramiko
from threading import Thread
import time
from distutils.util import strtobool
from socket import error as SocketError
from src.logger import get_heartbeat_logger, get_default_logger

timeout_default = 3.0


class SUTMonitor(Thread):
    def __init__(self, pid, remote_host, username, password=None, host_keys=None, auto_policy=True, interval=2.0):
        Thread.__init__(self)
        if type(pid) is list:
            self._pid_list = pid
        else:
            self._pid_list = [pid]

        self._remote = remote_host
        self._username = username
        self._password = password
        self._interval = interval
        self._is_running = False

        self._heartbeat_logger = get_heartbeat_logger()
        self._logger = get_default_logger()

        self._ssh = paramiko.SSHClient()
        if host_keys:
            self._ssh.load_host_keys(host_keys)
        else:
            self._ssh.load_system_host_keys()

        if auto_policy:
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @property
    def is_running(self):
        return self._is_running

    def stop(self):
        self._is_running = False

    def run(self):
        self._logger.info('Start SUT Monitor for: {}@{} pid={}'.format(self._username, self._remote, self._pid_list))
        try:
            self._ssh.connect(self._remote, username=self._username, password=self._password, timeout=timeout_default)
            self._is_running = True
            stdin, stdout, stderr = self._ssh.exec_command('python3', get_pty=True)

            # hacky read the 3 initial lines of Python REPL
            # might block if initial amount of output lines of Python changes
            remote_py_version = stdout.readline().strip()
            remote_gcc_version = stdout.readline().strip()
            stdout.readline().strip()
            self._logger.info('SUT Monitor started remote Python REPL: {} gcc={}'
                              .format(remote_py_version, remote_gcc_version))

            # prepare the REPL with imports and required variables
            # see psutil docs for more information about attributes and output
            # https://psutil.readthedocs.io/en/latest/
            execute_command(stdin, stdout, 'import psutil as pu')
            execute_command(stdin, stdout, 'from datetime import datetime')
            execute_command(stdin, stdout, 'import json')

            execute_command(stdin, stdout, "attrs=['pid','status','cpu_num','cpu_percent','cpu_times','name',"
                                           "'io_counters','num_threads','username','connections','memory_percent',"
                                           "'memory_info','num_ctx_switches','num_fds','open_files']")
            execute_command(stdin, stdout, 'processes = dict()')

            pid_counter = 0
            for pid in self._pid_list:
                # check if the specified PID exists
                if pid_exists(stdin, stdout, pid):
                    # create pu.Process object to monitor the process with the PID
                    execute_command(stdin, stdout, 'processes["{}"] = pu.Process({})'.format(pid, pid))
                    pid_counter += 1
                else:
                    self._logger.warning('Process with pid={} does not exist'.format(pid))

            if pid_counter == 0:
                self._logger.warning('No valid processes to monitor')
                self.stop()

            while self._is_running:
                for pid in self._pid_list:
                    if pid_exists(stdin, stdout, pid):
                        execute_command(stdin, stdout, 'p = processes["{}"]'.format(pid))
                        execute_command(stdin, stdout, 'out = p.as_dict(attrs=attrs)')
                        execute_command(stdin, stdout, 'out["ts"] = datetime.now().timestamp()')
                        execute_command(stdin, stdout, 'print(json.dumps(out))')

                        # now read the output
                        line = stdout.readline().strip()
                        self._heartbeat_logger.sut_heartbeat(line)
                    else:
                        # process not alive anymore
                        self._logger.warning('Process with pid={} does not exist anymore'.format(pid))
                        # remove from local pid_list
                        self._pid_list.remove(pid)
                        # and remove from remote list of pu.Processes
                        execute_command(stdin, stdout, 'del processes["{}"]'.format(pid))

                # check the length of active processes and stop if no more processes to monitor
                if len(self._pid_list) == 0:
                    self._logger.info('No more active processes to monitor')
                    self.stop()
                else:
                    time.sleep(self._interval)

        except SocketError as ex:
            self._logger.error(ex)
        except paramiko.ssh_exception.BadHostKeyException as ex:
            self._logger.error(ex)
        except paramiko.ssh_exception.AuthenticationException as ex:
            self._logger.error(ex)
        except Exception as ex:
            self._logger.error('Unknown Exception: {}'.format(ex))

        self._logger.info('Close SSH connection of SUT Monitor')
        self._ssh.close()


def pid_exists(stdin, stdout, pid):
    # processes might die during monitoring or be not existent at all!
    execute_command(stdin, stdout, 'pu.pid_exists({})'.format(pid))
    line = stdout.readline().strip()  # get the response
    exists = bool(strtobool(line))    # convert the string to bool object
    return exists


def execute_command(stdin, stdout, command):
    """
    executes a command within the REPL on the remote machine over stdin
    :param stdin:
    :param stdout:
    :param command:
    :return:
    """
    stdin.write(command + '\n')
    stdin.flush()
    reached = False

    while not reached:
        ret = stdout.readline()
        if ret.startswith('>>> '):
            reached = True
