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
import datetime
from collections import namedtuple
import src.utils.header_helper as ph
from src.proxy.tcp_proxy import StreamProxy
from src.proxy.udp_proxy import DatagramProxy
from src.logger import log_dir_rel

listen_if = '0.0.0.0'


# TODO: what about replacing the default event loop with uvloop to speed up async operations?
# https://github.com/MagicStack/uvloop
def __start_stream_proxy(local_addr, remote_addr, fuzzer):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: StreamProxy(remote_addr, fuzzer), local_addr.host, local_addr.port)
    asyncio.ensure_future(coro)


def __start_datagram_proxy(local_addr, remote_addr, fuzzer):
    loop = asyncio.get_event_loop()
    coro = loop.create_datagram_endpoint(lambda: DatagramProxy(remote_addr, fuzzer),
                                         local_addr=local_addr)
    asyncio.ensure_future(coro)


def start_proxy(local_port, remote_host, remote_port, fuzzer):
    # check if we need to start a stream proxy or a datagram proxy
    # get the pre-defined IPL4 transport type from protocol description
    transport = fuzzer.codec.protocol_description.ipl4_transport
    if transport == 'tcp':
        proxy = __start_stream_proxy
    elif transport == 'udp':
        proxy = __start_datagram_proxy
    else:
        # this case should never happen
        print('Only TCP or UDP transport possible')
        return

    address = namedtuple('address', ['host', 'port'])
    remote_addr = address(remote_host, remote_port)
    local_addr = address(listen_if, local_port)

    t1 = datetime.datetime.now()
    proto_type = fuzzer.codec.protocol_description.protocol_type
    ph.print_proxy_header(transport, proto_type, local_addr, remote_addr)

    loop = asyncio.get_event_loop()
    proxy(local_addr, remote_addr, fuzzer)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        runtime = datetime.datetime.now() - t1
        ph.print_proxy_footer(transport, proto_type, local_addr, remote_addr, runtime, log_dir_rel)

    loop.close()
