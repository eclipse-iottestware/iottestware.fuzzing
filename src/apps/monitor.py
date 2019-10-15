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
from src.monitor.sut_monitor import SUTMonitor
from src.logger import get_default_logger


def ssh_monitor(args):
    logger = get_default_logger()
    remote_host = args.remote_host
    pid = args.pid
    username = args.user

    # TODO: still required?
    # KNOWN_HOSTS = '~/.ssh/known_hosts'
    # known_hosts = os.path.expanduser(KNOWN_HOSTS)

    mon = SUTMonitor(pid, remote_host, username)
    mon.start()

    try:
        mon.join()
    except KeyboardInterrupt:
        logger.info('Caught KeyboardInterrupt: closing monitoring')
        mon.stop()
