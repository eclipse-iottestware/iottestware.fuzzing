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

import os
import json
import re
import socket
import datetime as dt

from src.statistics.rotated_file import get_rotated_files
from src.logger import filename_heartbeat, get_default_logger, time_format

hb_regex = re.compile(r'(?=)(([0-9]{2}:){2}[0-9]{2}.[0-9]{3}:(?<=)\s)(\{.*)')


class HeartbeatLog:

    def __init__(self, log_dir):
        self._log_dir = log_dir
        self._processes = dict()
        self._logger = get_default_logger()

    @property
    def process_pids(self):
        return self._processes.keys()

    @property
    def num_processes(self):
        return len(self.process_pids)

    def get_process_name(self, pid):
        if pid in self._processes:
            return self._processes[pid]['name']

    def get_process_user(self, pid):
        if pid in self._processes:
            return self._processes[pid]['user']

    #
    def get_start_timestamp_log(self, pid):
        if pid in self._processes:
            log_time_str = self._processes[pid]['start_log']
            timestamp = dt.datetime.strptime(log_time_str, time_format + '.%f')
            return timestamp

    def get_start_timestamp_sut(self, pid):
        if pid in self._processes:
            return self._processes[pid]['start_sut']

    def get_heartbeat(self, pid):
        if pid in self._processes:
            return self._processes[pid]['heartbeat']
        else:
            return []

    def get_ticks(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.timestamp_2 for e in hb]

    def get_cpu_percent(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.cpu_percent for e in hb]

    def get_avg_cpu(self, pid):
        if pid in self._processes:
            return self._processes[pid]['avg_cpu']
        else:
            return -1.0

    def get_mem_percent(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.mem_percent for e in hb]

    def get_avg_mem(self, pid):
        if pid in self._processes:
            return self._processes[pid]['avg_mem']
        else:
            return -1.0

    def get_mem_info(self, pid):
        """
        get several memory informations at once
        :param pid: PID of the process
        :return: dict with separated lists for each mem_info
        """
        hb = self.get_heartbeat(pid)
        ret = dict()
        ret['percent'] = list()
        ret['rss'] = list()
        ret['text'] = list()
        ret['data'] = list()
        ret['lib'] = list()
        ret['vms'] = list()
        ret['dirty'] = list()

        for e in hb:
            ret['percent'].append(e.mem_percent)
            ret['rss'].append(e.mem_rss)
            ret['text'].append(e.mem_text)
            ret['data'].append(e.mem_data)
            ret['lib'].append(e.mem_lib)
            ret['vms'].append(e.mem_vms)
            ret['dirty'].append(e.mem_dirty)

        return ret

    def get_mem_rss(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.mem_rss for e in hb]

    def get_mem_vms(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.mem_rss for e in hb]

    def get_mem_text(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.mem_text for e in hb]

    def get_mem_lib(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.mem_lib for e in hb]

    def get_mem_data(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.mem_data for e in hb]

    def get_mem_dirty(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.mem_dirty for e in hb]

    def get_num_connections(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.num_connections for e in hb]

    def get_num_threads(self, pid):
        hb = self.get_heartbeat(pid)
        return [e.num_threads for e in hb]

    def get_io_count(self, pid, absolute=False):
        hb = self.get_heartbeat(pid)
        ret = dict()
        ret['read'] = list()
        ret['write'] = list()
        last_read = None   # initial reads
        last_write = None  # initial writes
        for e in hb:
            read = e.io_read_count
            write = e.io_write_count

            if not absolute:
                if last_read is None:
                    last_read = read
                if last_write is None:
                    last_write = write

                diff_read = read - last_read
                diff_write = write - last_write
                last_read = read
                last_write = write
            else:
                diff_read = read
                diff_write = write

            ret['read'].append(diff_read)
            ret['write'].append(diff_write)

        return ret

    def get_io_bytes(self, pid, absolute=False):
        hb = self.get_heartbeat(pid)
        ret = dict()
        ret['read'] = list()
        ret['write'] = list()
        last_read = None   # initial reads
        last_write = None  # initial writes
        for e in hb:
            read = e.io_read_bytes
            write = e.io_write_bytes

            if not absolute:
                if last_read is None:
                    last_read = read
                if last_write is None:
                    last_write = write

                diff_read = read - last_read
                diff_write = write - last_write
                last_read = read
                last_write = write
            else:
                diff_read = read
                diff_write = write

            ret['read'].append(diff_read)
            ret['write'].append(diff_write)

        return ret

    def parse(self):
        """
        Parse the logfiles from the given log_dir and prepare for further processing
        :return: True if parsed successfully, False otherwise
        """
        ret = self.__parse_heartbeat_log()

        return ret

    def __parse_heartbeat_log(self):
        heartbeat_path = os.path.join(self._log_dir, filename_heartbeat)
        if not os.path.isfile(heartbeat_path) or not os.path.exists(heartbeat_path):
            self._logger.error('{} does not exist or is not a file'.format(heartbeat_path))
            return False

        files = get_rotated_files(heartbeat_path)
        for hb_log_file in files:
            with open(hb_log_file) as f:
                for l in f:
                    matches = hb_regex.finditer(l)
                    for i, m in enumerate(matches):
                        log_timestamp = m.group(1).strip()[:-1]  # timestamp of the logevent
                        hb = json.loads(m.group(3))  # the heartbeat event

                        pid = hb['pid']
                        if pid not in self._processes:
                            # new PID discovered in log
                            start_ts = hb['ts']  # required to normalize the time
                            pname = hb['name']
                            username = hb['username']

                            process = {'pid': pid, 'name': pname, 'user': username,
                                       'start_log': log_timestamp, 'start_sut': start_ts,
                                       'avg_cpu': 0.0, 'avg_mem': 0.0, 'heartbeat': list()}
                            self._processes[pid] = process

                        process = self._processes[pid]
                        phb = process['heartbeat']
                        event = HeartbeatEvent(log_timestamp, start_ts, hb)

                        # calculate averages
                        process['avg_cpu'] = (len(phb) * process['avg_cpu'] + event.cpu_percent) / (len(phb) + 1)
                        process['avg_mem'] = (len(phb) * process['avg_mem'] + event.mem_percent) / (len(phb) + 1)

                        phb.append(event)

        return True


class HeartbeatEvent:
    """
    HeartbeatEvent structures an json event object for easier access
    """
    def __init__(self, log_ts, start_ts, hb):
        self._log_timestamp = log_ts        # timestamp when the logevent occurred on the test system
        self._sut_timestamp = hb['ts']      # timestamp of the event on the system under test
        self._sut_start_ts = start_ts
        self._pid = hb['pid']               # TODO: should never change, still required here?
        # self._process_name = hb['name']   # should never change
        self._status = hb['status']
        # self._username = hb['username']   # should never change
        self._cpu_percent = hb['cpu_percent']
        self._mem_percent = hb['memory_percent']
        self._num_threads = hb['num_threads']
        self._num_fds = hb['num_fds']

        # network connections
        # https://psutil.readthedocs.io/en/latest/#psutil.Process.connections
        self._connections = list()
        for con in hb['connections']:
            fd = con[0]

            # fix: psutils encodes AF_INET6 with 10, corresponds with 30 in socket.AddressFamily
            af_inet_idx = con[1] if (con[1] != 10) else 30
            address_family = socket.AddressFamily(af_inet_idx).name
            socket_kind = socket.SocketKind(con[2]).name

            listen_addr = con[3]
            if len(listen_addr) > 0:
                laddr = {'ip': listen_addr[0], 'port': listen_addr[1]}
            else:
                laddr = {'ip': '', 'port': ''}

            remote_addr = con[4]
            if len(remote_addr) > 0:
                raddr = {'ip': remote_addr[0], 'port': remote_addr[1]}
            else:
                raddr = {'ip': '', 'port': ''}

            status = con[5]

            con_dict = {'fd': fd, 'family': address_family, 'type': socket_kind, 'laddr': laddr,
                        'raddr': raddr, 'status': status}
            self._connections.append(con_dict)

        # Memory consumption
        # https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_full_info
        # http://grodola.blogspot.com/2016/02/psutil-4-real-process-memory-and-environ.html
        mem_info = hb['memory_info']
        mem_rss = mem_info[0] / (1024*1024)
        mem_vms = mem_info[1] / (1024*1024)
        mem_shared = mem_info[2] / (1024*1024)
        mem_text = mem_info[3] / (1024*1024)
        mem_lib = mem_info[4] / (1024*1024)
        mem_data = mem_info[5] / (1024*1024)
        mem_dirty = mem_info[6] / (1024*1024)
        self._memory = {'rss': mem_rss, 'vms': mem_vms, 'shared': mem_shared, 'text': mem_text,
                        'lib': mem_lib, 'data': mem_data, 'dirty': mem_dirty}

        # I/O
        # https://psutil.readthedocs.io/en/latest/#psutil.Process.io_counters
        io_counters = hb['io_counters']
        io_read_count = io_counters[0]
        io_write_count = io_counters[1]
        io_read_chars = io_counters[4]   # bytes read via syscalls
        io_write_chars = io_counters[5]  # bytes written via syscalls
        self._io_counters = {'read_count': io_read_count, 'write_count': io_write_count,
                             'read_chars': io_read_chars, 'write_chars': io_write_chars}

        # CPU times
        # https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_times
        cpu_times = hb['cpu_times']
        self._cpu_times = {'user': cpu_times[0], 'system': cpu_times[1], 'children_user': cpu_times[2],
                           'children_system': cpu_times[3]}

        # Context switches
        # https://psutil.readthedocs.io/en/latest/#psutil.Process.num_ctx_switches
        ctx_switches = hb['num_ctx_switches']
        self._ctx_switches = {'voluntary': ctx_switches[0], 'involuntary': ctx_switches[1]}

        # Open files
        # https://psutil.readthedocs.io/en/latest/#psutil.Process.open_files
        open_files = hb['open_files']
        self._open_files = list()
        for f in open_files:
            self._open_files.append({'path': f[0], 'fd': f[1], 'pos': f[2], 'mode': f[3], 'flags': f[4]})

    def __str__(self):
        ret = '({}) status={}, cpu={}%, mem={}%'.format(self.timestamp, self.status, self.cpu_percent, self.mem_percent)
        return ret

    @property
    def timestamp_log(self):
        return self._log_timestamp

    @property
    def timestamp_sut(self):
        return self._sut_timestamp

    @property
    def timestamp(self):
        """
        use timestamp_sut as default
        :return: the timestamp captured on the SUT
        """
        return self.timestamp_sut

    @property
    def timestamp_2(self):
        """
        TODO: chose better name... time elapsed since start of monitoring
        :return:
        """
        return self.timestamp_sut - self._sut_start_ts

    def datetime(self, fmt=None, tz: dt.timezone = dt.timezone.utc):
        """
        get the default timestamp as formatted datetime
        :param fmt: format string
        :param tz:	timezone
        :return:
        """
        ret = dt.datetime.fromtimestamp(self.timestamp, tz=tz)

        if fmt:
            return ret.strftime(fmt)
        else:
            return ret

    @property
    def pid(self):
        return self._pid

    @property
    def status(self):
        return self._status

    @property
    def cpu_percent(self):
        return self._cpu_percent

    @property
    def cpu_times(self):
        return self._cpu_times

    @property
    def mem_percent(self):
        """
        :return: How many percent of the whole memory used by this process
        """
        return self._mem_percent

    @property
    def mem_info(self):
        """
        Memory info contains all types of memory packed as a dictionary
        :return: dict of memory information containing RSS, VMS, Shared, Lib etc.
        """
        return self._memory

    @property
    def mem_rss(self):
        """
        :return: "Real" process memory info
        """
        return self._memory['rss']

    @property
    def mem_vms(self):
        """
        :return: Virtual Memory System
        """
        return self._memory['vms']

    @property
    def mem_text(self):
        """
        :return: Memory used by executable code
        """
        return self._memory['text']

    @property
    def mem_lib(self):
        """
        :return: Memory used by shared libraries
        """
        return self._memory['lib']

    @property
    def mem_data(self):
        """
        :return: Memory used by data
        """
        return self._memory['data']

    @property
    def mem_dirty(self):
        """
        :return: Memory used by dirty pages
        """
        return self._memory['dirty']

    @property
    def connections(self):
        return self._connections

    @property
    def num_connections(self):
        return len(self.connections)

    @property
    def num_threads(self):
        return self._num_threads

    @property
    def num_fds(self):
        return self._num_fds

    @property
    def num_open_files(self):
        return len(self.open_files)

    @property
    def open_files(self):
        return self._open_files

    @property
    def io_counters(self):
        return self._io_counters

    @property
    def io_read_count(self):
        return self._io_counters['read_count']

    @property
    def io_write_count(self):
        return self._io_counters['write_count']

    @property
    def io_read_bytes(self):
        return self._io_counters['read_chars']

    @property
    def io_write_bytes(self):
        return self._io_counters['write_chars']
