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
import matplotlib.pyplot as plt

import src.utils.header_helper as ph
from src.statistics.heartbeat_log import HeartbeatLog
from src.statistics.fuzzer_log import FuzzingLog

r_heartbeat = r'(?=)(([0-9]{2}:){2}[0-9]{2}.[0-9]{3}:(?<=)\s)(\{.*)'

X_LABEL = 'time (s)'


def logstats(args):
    log_dir = os.path.abspath(args.directory)

    fig_dir = os.path.join(log_dir, 'figures')
    if not os.path.exists(fig_dir) and args.save:
        os.mkdir(fig_dir)

    fl = FuzzingLog(log_dir)
    log_state = fl.parse()

    if log_state:
        header = 'Rules engine statistics:'
        ph.print_header(header)
        print('>> Found {} triggered rules'.format(fl.num_rules))
        ts_stats = list()
        labels = list()

        for idx, rule_id in enumerate(fl.rule_ids):
            timestamps = fl.get_rule_appearances(rule_id)
            ts_stats.append(len(timestamps))
            labels.append(rule_id)
            info = '({}) "{}" triggered {} times:'.format(idx, rule_id, len(timestamps))
            print(info)

        plt.figure('rules_engine_pi')
        plt.title('Rules engine')
        plt.pie(ts_stats, labels=labels, autopct=lambda p: '{:.2f}%'.format(p))
        if args.save:
            fig_path = os.path.join(fig_dir, 'rules_engine_pie.png')
            plt.savefig(fig_path)

    # process the heartbeat logs
    hbl = HeartbeatLog(log_dir)
    log_state = hbl.parse()

    if log_state:
        header = 'SUT statistics:'
        ph.print_header(header)
        pids = hbl.process_pids
        print('{} processes were monitored: {}'.format(len(pids), list(pids)))

        # plot heartbeats for each process
        for pid in pids:
            pname = hbl.get_process_name(pid)

            x_td = hbl.get_ticks(pid)

            # Summary
            y_cpu_percent = hbl.get_cpu_percent(pid)
            y_mem_percent = hbl.get_mem_percent(pid)

            plt.figure('summary_{}'.format(pid))
            plt.title('Performance Summary: {}'.format(pname))
            plt.plot(x_td, y_cpu_percent, label='CPU usage in %')
            plt.plot(x_td, y_mem_percent, label='Memory usage in %')
            plt.legend(loc='upper right')
            plt.ylabel('%')
            plt.xlabel(X_LABEL)

            if args.save:
                fig_path = os.path.join(fig_dir, 'summary_{}.png'.format(pname))
                plt.savefig(fig_path)

            # Network connections
            plt.figure('connections_{}'.format(pid))
            plt.title('Network Connections: {}'.format(pname))
            plt.plot(x_td, hbl.get_num_connections(pid), label='connections')
            # plt.plot(x_td, lfp.get_num_threads(pid), label='threads')  # own plot for threads?
            plt.ylabel('#')
            plt.legend(loc='upper right')
            plt.xlabel(X_LABEL)
            if args.save:
                fig_path = os.path.join(fig_dir, 'network_{}.png'.format(pname))
                plt.savefig(fig_path)

            # Memory consumption
            mem = hbl.get_mem_info(pid)
            plt.figure('memory_{}'.format(pid))
            plt.title('Memory usage: {}'.format(pname))
            plt.plot(x_td, mem['rss'], label='Resident Set Size')
            plt.plot(x_td, mem['text'], label='Executable Code')
            plt.plot(x_td, mem['data'], label='Data')
            # needed? VMS usually much higher then other memory usages -> less detailed RSS/text/data usage
            # plt.plot(x_td, mem['vms'], label='Virtual Memory System')
            plt.plot(x_td, mem['lib'], label='Shared Libraries')
            plt.plot(x_td, mem['dirty'], label='Dirty pages')
            plt.legend(loc='upper right')
            plt.xlabel(X_LABEL)
            plt.ylabel('MB')
            if args.save:
                fig_path = os.path.join(fig_dir, 'memory_{}.png'.format(pname))
                plt.savefig(fig_path)

            # I/O operations
            io_operations = hbl.get_io_count(pid, absolute=False)
            plt.figure('io_count_{}'.format(pid))
            plt.title('I/O operations: {}'.format(pname))
            plt.plot(x_td, io_operations['read'], label='Read')
            plt.plot(x_td, io_operations['write'], label='Write')
            plt.legend(loc='upper right')
            plt.xlabel(X_LABEL)
            plt.ylabel('#')
            if args.save:
                fig_path = os.path.join(fig_dir, 'io_operations_{}.png'.format(pname))
                plt.savefig(fig_path)

            # I/O amount of bytes
            io_operations = hbl.get_io_bytes(pid, absolute=False)
            plt.figure('io_bytes_{}'.format(pid))
            plt.title('I/O: {}'.format(pname))
            plt.plot(x_td, io_operations['read'], label='Read')
            plt.plot(x_td, io_operations['write'], label='Write')
            plt.legend(loc='upper right')
            plt.xlabel(X_LABEL)
            plt.ylabel('Bytes')
            if args.save:
                fig_path = os.path.join(fig_dir, 'io_bytes_{}.png'.format(pname))
                plt.savefig(fig_path)

            print('>> {}(pid={}) average: CPU={:.4f}% Memory={:.4f}%'
                  .format(pname, pid, hbl.get_avg_cpu(pid), hbl.get_avg_mem(pid)))

    if args.show:
        plt.show()
