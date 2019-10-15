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

from enum import Enum


class TrafficDirection(Enum):
    CLIENT_2_PROXY = 0,
    PROXY_2_SERVER = 1,
    SERVER_2_PROXY = 2,
    PROXY_2_CLIENT = 3

    def __str__(self):
        if self is TrafficDirection.CLIENT_2_PROXY:
            return 'Client->Proxy'
        elif self is TrafficDirection.PROXY_2_SERVER:
            return 'Proxy->Server'
        elif self is TrafficDirection.SERVER_2_PROXY:
            return 'Proxy<-Server'
        elif self is TrafficDirection.PROXY_2_CLIENT:
            return 'Client<-Proxy'
        else:
            return 'UNKNOWN'


class ProxyTrafficEvent:
    # ProxyTrafficEvent is used for logging the traffic with peername and direction of the data
    def __init__(self, peer, direction):
        self._peer = peer
        self._direction = direction

    def __str__(self):
        if self._direction is TrafficDirection.CLIENT_2_PROXY:
            return '{}->Proxy'.format(self._peer)
        elif self._direction is TrafficDirection.PROXY_2_SERVER:
            return 'Proxy->{}'.format(self._peer)
        elif self._direction is TrafficDirection.SERVER_2_PROXY:
            return 'Proxy<-{}'.format(self._peer)
        elif self._direction is TrafficDirection.PROXY_2_CLIENT:
            return '{}<-Proxy'.format(self._peer)
        else:
            return 'UNKNOWN'
