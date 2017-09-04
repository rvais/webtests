#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import logging  # python logging module
import os       # environment variables of the shell/machine and shell utils
import errno

# definiton of var & const_____________________________________________

DEFAULT_LOG_LEVEL = logging.DEBUG  # CRITICAL | ERROR | WARNING | INFO | NOTSET
PATH_TO_LOGS = './logs'

def get_logger(name="logger", level=None, sfx=None):
    logpath = make_path_for_logs()
    if sfx is not None:
        name = "{}{}".format(name, sfx)

    logger = logging.getLogger(name)
    logname = "{}.log".format(name)

    # logging level for whole logger
    # can change log level in a subsequent call
    logger.setLevel(DEFAULT_LOG_LEVEL)

    if level is not None:
        logger.setLevel(level)

    if not logger.hasHandlers():
        # handler for stderr
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s]: %(message)s')
        handler.setFormatter(formatter)
        # handler.setLevel(logging.ERROR) # only errors are needed
        logger.addHandler(handler)

        # handler for logging to file
        handler = logging.FileHandler(os.path.join(logpath, logname))
        formatter = logging.Formatter('%(asctime)s|[%(levelname)s]'
                                          ' %(name)s: %(message)s')
        handler.setFormatter(formatter)
        # logs everything that goes to the logger
        logger.addHandler(handler)

    return logger

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
