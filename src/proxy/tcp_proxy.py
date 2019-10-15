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


class StreamProxy(asyncio.Protocol):

    def __init__(self, remote_address, fuzzer):
        self._remote_address = remote_address
        self._peername = None
        self._proto_module = fuzzer.codec
        self._fuzzing_engine = fuzzer.fuzzing_engine
        self._transport = None
        self._remote = None
        self._logger = get_default_logger()
        self._traffic_logger = get_traffic_logger()
        super().__init__()

    def connection_made(self, transport):
        self._transport = transport
        host, port = transport.get_extra_info('peername')
        self._peername = '{}:{}'.format(host, port)
        traffic_event_log = 'Client connected'
        self._traffic_logger.ipl4_event(ProxyTrafficEvent(self._peername,
                                                          TrafficDirection.CLIENT_2_PROXY), traffic_event_log)

    def connection_lost(self, exc):
        traffic_event_log = 'Client closed network connection'
        self._traffic_logger.ipl4_event(ProxyTrafficEvent(self._peername,
                                                          TrafficDirection.CLIENT_2_PROXY), traffic_event_log)
        if self._remote:
            self._remote.close_to_remote(exc)

    def close_from_remote(self, exc):
        traffic_event_log = 'Server closed network connection'
        remote_peer = '{}:{}'.format(self._remote_address.host, self._remote_address.port)
        self._traffic_logger.ipl4_event(ProxyTrafficEvent(remote_peer,
                                                          TrafficDirection.SERVER_2_PROXY), traffic_event_log)
        self._transport.close()

    def data_received(self, data):
        self._logger.info('received {}B from {}'.format(len(data), self._peername))

        if self._remote is None:
            loop = asyncio.get_event_loop()
            self._remote = RemoteStreamEndpoint(self)
            remote_host, remote_port = self._remote_address
            coro = loop.create_connection(lambda: self._remote, remote_host, remote_port)
            asyncio.ensure_future(coro)

        self._traffic_logger.raw_traffic(ProxyTrafficEvent(self._peername, TrafficDirection.CLIENT_2_PROXY), data)
        message = self._proto_module.decode_data(data)
        mutated = self._fuzzing_engine.fuzz_request(message)

        # if fuzzing engine applied mutations, get the new encoded data
        if mutated:
            data = self._proto_module.encode_message(message)

        # forward the data via RemoteDatagramEndpoint
        remote_endpoint = self._remote
        asyncio.ensure_future(remote_endpoint.data_to_remote(data))  # run async as concurrent task

    def data_from_remote(self, data):
        message = self._proto_module.decode_data(data)
        mutated = self._fuzzing_engine.fuzz_response(message)

        # if fuzzing engine applied mutations, get the new encoded data
        if mutated:
            data = self._proto_module.encode_message(message)

        self._traffic_logger.raw_traffic(ProxyTrafficEvent(self._peername, TrafficDirection.PROXY_2_CLIENT), data)
        self._transport.write(data)


class RemoteStreamEndpoint(asyncio.Protocol):

    def __init__(self, proxy):
        self._proxy = proxy
        self._transport = None
        self._peername = None
        self._logger = get_default_logger()
        self._traffic_logger = get_traffic_logger()

    def connection_made(self, transport):
        self._transport = transport
        host, port = transport.get_extra_info('peername')
        self._peername = '{}:{}'.format(host, port)
        traffic_event_log = 'connection made to Server'
        self._traffic_logger.ipl4_event(ProxyTrafficEvent(self._peername,
                                                          TrafficDirection.PROXY_2_SERVER), traffic_event_log)

    def _is_connected(self):
        if self._transport is None:
            return False
        elif self._transport.is_closing():
            return False    # transport is closing
        else:
            return True     # transport is created and not closed

    async def _probe_transport(self):
        """
        if the client connects and sends data immediately, the connection to the server might not be established yet
        retry and check until self.server_transport was created
        :return: True if connection was created and not closed
        """
        if self._is_connected():
            return True

        connected = False
        retries = 5
        sleep_timer = 0.1
        counter = 0
        while retries > counter:
            counter += 1
            connected = self._is_connected()
            if not connected:
                await asyncio.sleep(counter * sleep_timer)
            else:
                break

        return connected

    async def data_to_remote(self, data):
        """
        Forward data received and fuzzed by the proxy to remote endpoint
        :param data:
        :return:
        """
        connected = await self._probe_transport()
        if connected:
            self._traffic_logger.raw_traffic(ProxyTrafficEvent(self._peername, TrafficDirection.PROXY_2_SERVER), data)
            self._transport.write(data)
        else:
            self._logger.info('remote transport connection could not be established: {}'.format(self._transport))
            if self._transport:
                self._transport.close()

    def close_to_remote(self, exc):
        if self._transport:
            self._logger.info('close remote connection: exc={} / transport={}'.format(exc, self._transport))
            self._transport.close()

    def connection_lost(self, exc):
        self._logger.info('remote connection closed: exc={} / transport={}'.format(exc, self._transport))
        self._proxy.close_from_remote(exc)

    def data_received(self, data):
        self._logger.info('received {}B from {}'.format(len(data), self._peername))

        self._traffic_logger.raw_traffic(ProxyTrafficEvent(self._peername, TrafficDirection.SERVER_2_PROXY), data)
        self._proxy.data_from_remote(data)
