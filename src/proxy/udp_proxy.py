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

import asyncio

from src.logger import get_default_logger, get_traffic_logger
from src.proxy.proxy_events import TrafficDirection, ProxyTrafficEvent


class DatagramProxy(asyncio.DatagramProtocol):

    def __init__(self, remote_address, fuzzer):
        self._remote_address = remote_address
        self._proto_module = fuzzer.codec
        self._fuzzing_engine = fuzzer.fuzzing_engine
        self._remotes = {}
        self._transport = None
        self._logger = get_default_logger()
        self._traffic_logger = get_traffic_logger()
        super().__init__()

    @property
    def remotes(self):
        return self._remotes

    @property
    def transport(self):
        return self._transport

    def connection_made(self, transport):
        self._transport = transport

    def connection_lost(self, exc):
        self._logger.info('Connection lost: {}'.format(exc))

    def datagram_received(self, data, addr):
        self._logger.info('received {}B from {}'.format(len(data), addr))

        loop = asyncio.get_event_loop()
        if addr not in self.remotes:
            self._logger.info('create new remote endpoint for client={}'.format(addr))
            self._remotes[addr] = RemoteDatagramEndpoint(self)
            coro = loop.create_datagram_endpoint(lambda: self.remotes[addr], remote_addr=self._remote_address)
            asyncio.ensure_future(coro)

        self._traffic_logger.raw_traffic(ProxyTrafficEvent(addr, TrafficDirection.CLIENT_2_PROXY), data)
        message = self._proto_module.decode_data(data)
        mutated = self._fuzzing_engine.fuzz(message)

        # if fuzzing engine applied mutations, get the new encoded data
        if mutated:
            data = self._proto_module.encode_message(message)

        # forward the data via RemoteDatagramEndpoint
        remote_endpoint = self._remotes[addr]
        asyncio.ensure_future(remote_endpoint.to_remote(data))  # run async as concurrent task

    def from_remote(self, data, addr):
        message = self._proto_module.decode_data(data)
        mutated = self._fuzzing_engine.fuzz(message)

        # if fuzzing engine applied mutations, get the new encoded data
        if mutated:
            data = self._proto_module.encode_message(message)

        self._traffic_logger.raw_traffic(ProxyTrafficEvent(addr, TrafficDirection.PROXY_2_CLIENT), data)
        self._transport.sendto(data, addr)


class RemoteDatagramEndpoint(asyncio.DatagramProtocol):

    def __init__(self, proxy):
        self._proxy = proxy
        self._transport = None
        self._peername = None
        self._logger = get_default_logger()
        self._traffic_logger = get_traffic_logger()
        super().__init__()

    @property
    def transport(self):
        return self._transport

    def connection_made(self, transport):
        self._transport = transport
        host, port = transport.get_extra_info('peername')
        self._peername = '{}:{}'.format(host, port)

    def _is_connected(self):
        if self._transport is not None:
            return True
        else:
            return False

    async def _probe_transport(self):
        if self._is_connected():
            return True

        connected = False
        retries = 5
        while retries > 0:
            retries -= 1
            connected = self._is_connected()
            if not connected:
                await asyncio.sleep(0.1)
            else:
                break

        return connected

    async def to_remote(self, data):
        """
        Forward data received and fuzzed by the proxy to remote endpoint
        :param data:
        :return:
        """
        connected = await self._probe_transport()
        if connected:

            self._traffic_logger.raw_traffic(ProxyTrafficEvent(self._peername, TrafficDirection.PROXY_2_SERVER), data)
            self._transport.sendto(data)
        else:
            raise Exception('Remote Transport could not be established')

    def datagram_received(self, data, addr):
        self._logger.info('received {}B from {}'.format(len(data), addr))

        self._traffic_logger.raw_traffic(ProxyTrafficEvent(self._peername, TrafficDirection.SERVER_2_PROXY), data)
        self._proxy.from_remote(data, addr)

    def connection_lost(self, exc):
        self._logger.info('connection lost from remote endpoint: {}'.format(exc))
        self._proxy.remotes.pop(self)
