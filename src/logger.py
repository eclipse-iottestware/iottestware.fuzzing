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
import shutil
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from logging import FileHandler

# create timestamped filenames for logfiles
start_time = datetime.now()
timestamp = start_time.strftime("%Y%m%d_%H_%M_%S")
filename_fuzzing = 'fuzzing_operations.log'
filename_raw_traffic = 'proxy_traffic.log'
filename_heartbeat = 'sut_heartbeat.log'
filename_build = 'build.log'

# create logging directories
log_base_dir = os.path.abspath('logs')
log_dir = os.path.join(log_base_dir, timestamp)
log_dir_rel = os.path.join('logs', timestamp)   # if a relative path is required, import this one

log_file_fuzzing = os.path.join(log_dir, filename_fuzzing)
log_file_traffic = os.path.join(log_dir, filename_raw_traffic)
log_file_heartbeat = os.path.join(log_dir, filename_heartbeat)
log_file_build = os.path.join(log_dir, filename_build)

# configuration for logfile handling
file_size_mb = 50
max_bytes = file_size_mb * 1024 * 1024
backup_count = 10  # (backup_count * file_size_mb) = max size of log files

time_format = '%H:%M:%S'
DEFAULT_LOGGING_FORMAT = '%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s: %(message)s'
logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=logging.ERROR, datefmt=time_format)

"""
Define a custom level for raw traffic logging
"""
BUILDER_ERROR_LVL_NUM = logging.ERROR + 6   # error which happen during building from configuration
BUILDER_WARN_LVL_NUM = logging.ERROR + 5    # warnings during build
FUZZING_OP_LVL_NUM = logging.ERROR + 4
IPL4_EVENT_LVL_NUM = logging.ERROR + 3
RAW_TRAFFIC_LVL_NUM = logging.ERROR + 2
HEARTBEAT_LEVEL_NUM = logging.ERROR + 1

logging.addLevelName(BUILDER_ERROR_LVL_NUM, 'BUILD_ERROR')
logging.addLevelName(BUILDER_WARN_LVL_NUM, 'BUILD_WARN')
logging.addLevelName(RAW_TRAFFIC_LVL_NUM, 'TRAFFIC')
logging.addLevelName(IPL4_EVENT_LVL_NUM, 'IPL4')
logging.addLevelName(FUZZING_OP_LVL_NUM, 'FUZZING')
logging.addLevelName(HEARTBEAT_LEVEL_NUM, 'HEARTBEAT')


def set_logging_level(log_level):
    logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=log_level, datefmt=time_format)


def raw_traffic(self, direction, message, *args, **kws):
    if self.isEnabledFor(RAW_TRAFFIC_LVL_NUM):
        oct_string = ''.join('{:02x}'.format(x) for x in message)
        oct_string = '\'' + oct_string + '\'O'  # make oct_string look like native TTCN-3 octetstrings
        self._log(RAW_TRAFFIC_LVL_NUM, oct_string, args, **kws, extra={'direction': direction})


def ipl4_event(self, direction, message, *args, **kws):
    if self.isEnabledFor(IPL4_EVENT_LVL_NUM):
        self._log(IPL4_EVENT_LVL_NUM, message, args, **kws, extra={'direction': direction})


def fuzzing_operation(self, rule_id, message, *args, **kws):
    if self.isEnabledFor(FUZZING_OP_LVL_NUM):
        self._log(FUZZING_OP_LVL_NUM, message, args, **kws, extra={'rule': rule_id})


def sut_heartbeat(self, message, *args, **kws):
    if self.isEnabledFor(HEARTBEAT_LEVEL_NUM):
        self._log(HEARTBEAT_LEVEL_NUM, message, args, **kws)


# bind the additional logging functions to the logger
logging.Logger.raw_traffic = raw_traffic
logging.Logger.ipl4_event = ipl4_event
logging.Logger.fuzzing_operation = fuzzing_operation
logging.Logger.sut_heartbeat = sut_heartbeat

# global logger instances
_traffic_logger = None
_fuzzing_logger = None
_heartbeat_logger = None
_factory_logger = None


def get_traffic_logger():
    """
    Function creates the traffic logger which will store to log to a file
    By that the logging of the raw network traffic is separated
    :return: traffic logger
    """
    global _traffic_logger  # only one single instance required!

    if _traffic_logger is None:
        log_format = '%(asctime)s.%(msecs)03d [%(direction)s]: %(message)s'
        formatter = logging.Formatter(log_format, time_format)

        _create_logging_dir()
        file_handler = RotatingFileHandler(log_file_traffic, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)

        _traffic_logger = logging.getLogger('network_traffic_logger')
        _traffic_logger.setLevel(RAW_TRAFFIC_LVL_NUM)
        _traffic_logger.addHandler(file_handler)

    return _traffic_logger


def get_fuzzing_logger():
    """
    Function creates the fuzzing event logger which will store to log to a file
    By that the logging of the fuzzing events is separated
    :return: fuzzing event logger
    """
    global _fuzzing_logger  # only one single instance required!

    if _fuzzing_logger is None:
        log_format = '%(asctime)s.%(msecs)03d [%(rule)s]: %(message)s'
        formatter = logging.Formatter(log_format, time_format)

        _create_logging_dir()
        file_handler = RotatingFileHandler(log_file_fuzzing, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)

        _fuzzing_logger = logging.getLogger('fuzzing_engine_logger')
        _fuzzing_logger.setLevel(FUZZING_OP_LVL_NUM)
        _fuzzing_logger.addHandler(file_handler)

    return _fuzzing_logger


def get_heartbeat_logger():
    """
    Function creates the heartbeat logger which will store to log to a file
    By that the logging of the heartbeat is separated
    :return: heartbeat logger
    """
    global _heartbeat_logger  # only one single instance required!

    if _heartbeat_logger is None:
        log_format = '%(asctime)s.%(msecs)03d: %(message)s'
        formatter = logging.Formatter(log_format, time_format)

        _create_logging_dir()
        file_handler = RotatingFileHandler(log_file_heartbeat, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)

        _heartbeat_logger = logging.getLogger('sut_heartbeat_logger')
        _heartbeat_logger.setLevel(HEARTBEAT_LEVEL_NUM)
        _heartbeat_logger.addHandler(file_handler)

    return _heartbeat_logger


def get_factory_logger():
    """
    Function creates a logger for the factory which will log the building/assembling process from configuration
    This logging information might be separated from other loggers for easier identification of configuration errors
    :return: factory logger
    """
    global _factory_logger
    log_to_file = False  # enable to configure?

    if log_to_file:
        if _factory_logger is None:
            log_format = '%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s'
            formatter = logging.Formatter(log_format, time_format)

            _create_logging_dir()
            file_handler = FileHandler(log_file_build)
            file_handler.setFormatter(formatter)

            _factory_logger = logging.getLogger('factory_logger')
            _factory_logger.addHandler(file_handler)
    else:
        _factory_logger = logging.getLogger('factory_logger')

    _factory_logger.setLevel(logging.WARN)
    return _factory_logger


def get_default_logger():
    logger = logging.getLogger('trace_logger')
    return logger


def remove_logging_dir():
    """
    Use with care as this function simply will remove the logging directory without checking
    if logs in the directory where present or required.
    Mainly used for situations where log files will be generated without any logging (e.g. validate configurations)
    """
    if not os.path.exists(log_base_dir):
        # nothing to delete, no logs/ directory
        return

    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)


def _create_logging_dir():
    if not os.path.exists(log_base_dir):
        os.mkdir(log_base_dir)

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
