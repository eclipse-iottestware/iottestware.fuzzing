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
import sys
import src.proxy as proxy
from src.factory import build_from_config as build
from src.monitor.sut_monitor import SUTMonitor


def proxy_fuzzer(args):
    local_port = args.local_port
    remote_host = args.remote_host

    mon = None  # SUT monitor!
    if bool(args.pid) or bool(args.user):
        if bool(args.user) != bool(args.pid):
            print('If PID is set, a username for the remote SUT is required')
            sys.exit()
        else:
            mon = SUTMonitor(args.pid, remote_host, args.user)

    if args.remote_port is None:
        if remote_host == '127.0.0.1' or remote_host == 'localhost':
            print('remote_port = local_port on localhost will result in a loop!')
            sys.exit()
        else:
            # otherwise use the same port
            # Note: loop still possible if you use your own IP
            remote_port = local_port
    else:
        remote_port = args.remote_port

    fuzzer = build(args.config)

    # start SUT monitor if requested
    if mon:
        mon.start()

    # proxy will start and loop until Ctrl+C
    proxy.start_proxy(local_port, remote_host, remote_port, fuzzer)

    # stop SUT monitor if started/created
    if mon:
        mon.stop()
