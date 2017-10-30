#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import os
import errno
import sys
import logging
from webtest.common.logging.levels import Level
from webtest.common.logging.outputs \
    import LOG_TO_CONSOLE, LOG_TO_FILE, LOG_TO_DEBUG_FILE, LOG_TO_TEST_FILE, LOG_TO_TRACE_FILE


PATH_TO_LOGS = "logs/"
FILE_BASE_NAME = os.path.basename(sys.argv[0])

_log_path_ = os.path.join(PATH_TO_LOGS, FILE_BASE_NAME)

__file_output_format = '[%(asctime)s][%(levelname)s] %(name)s: %(message)s'
__console_output_format = '[%(asctime)s][%(levelname)s] %(name)s: %(message)s'

__file_time_format = '%Y-%m-%d %H:%M:%S,'
__console_time_format = '%H:%M:%S'


# dictionaries with configuration of individual handlers
_console_handler_ = {
    'output' : sys.stderr,
    'time' : __console_time_format,
    'format' : __console_output_format,
    'level' : Level.DUMP,
}

_file_handler_ = {
    'output' : '{path}/{name}{ext}',
    'extension' : '.log',
    'time' : __file_time_format,
    'format' : __file_output_format,
    'level' : Level.DUMP,
}

_debug_handler_ = {
    'output' : '{path}/{name}{ext}',
    'extension' : '.debug.log',
    'time' : __file_time_format,
    'format' : __file_output_format,
    'level' : Level.DEBUG,
}

_trace_handler_ = {
    'output' : '{path}/{name}{ext}',
    'extension' : '.trace.log',
    'time' : __file_time_format,
    'format' : __file_output_format,
    'level' : Level.TRACE,
}

_test_handler_ = {
    'output' : '{path}/{name}{ext}',
    'extension' : '.test.log',
    'time' : __file_time_format,
    'format' : __file_output_format,
    'level' : Level.TRACE,
}

_output_handler_mapping = {
    LOG_TO_CONSOLE : _console_handler_,
    LOG_TO_FILE : _file_handler_,
    LOG_TO_DEBUG_FILE : _debug_handler_,
    LOG_TO_TRACE_FILE : _trace_handler_,
    LOG_TO_TEST_FILE : _test_handler_,
}

def make_path_for_logs(path=PATH_TO_LOGS):
    # taken from stack overflow
    # <http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python>
    try:
        os.makedirs(path)
    except OSError as exc:  # Python > 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    finally:
        return path

def parse_path(path: str) -> tuple:
    file_name = os.path.basename(path)
    extension = ''
    path = os.path.dirname(path)
    try:
        index = file_name.rfind('.')
        extension = file_name[index:]
        file_name = file_name[0:index]
    except ValueError as ex:
        pass

    return (path, file_name, extension)

def crate_handler(htype: str, path: str=_log_path_) -> object:
    htype = _output_handler_mapping[htype]
    if htype is None:
        raise ValueError("Unknown logging handler type.")

    if isinstance(htype['output'], str):
        path, file_name, extension = parse_path(path)
        make_path_for_logs(path)
        if extension != '.log':
            file_name = file_name + extension

        extension = htype['extension']
        path = htype['output'].format(path=path, name=file_name, ext=extension)
        handler = logging.FileHandler(path, 'a')
    else:
        handler = logging.StreamHandler()

    formatter = logging.Formatter(htype['format'], datefmt=htype['time'])
    handler.setLevel(htype['level'])
    handler.setFormatter(formatter)

    return handler








