#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.config.configurator import Configurator

import logging  # python logging module
from webtest.common.logging.levels import Level
from webtest.common.logging.logger_config import crate_handler, LOG_TO_TRACE_FILE, LOG_TO_TEST_FILE, LOG_TO_FILE, \
    LOG_TO_DEBUG_FILE, LOG_TO_CONSOLE



def get_logger(name: str="logger", level: int or None=None, sfx: str or None=None):
    if not isinstance(logging.getLoggerClass(), CustomLogger):
        logging.addLevelName(Level.TRACE, "TRACE")
        logging.TRACE = Level.TRACE
        logging.addLevelName(Level.DUMP, "DUMP")
        logging.DUMP = Level.DUMP
        logging.setLoggerClass(CustomLogger)

    if sfx is not None:
        name = "{}{}".format(name, sfx)

    logger = logging.getLogger(name)

    if level is not None:
        logger.setLevel(level)

    return logger



class CustomLogger(logging.Logger):

    def __init__(self,  *args, **kwargs):
        super(CustomLogger, self).__init__(*args, **kwargs)
        self.setLevel(Level.DUMP)
        self.__set_handlers()

    def trace(self, msg, *args, **kwargs):
        self.log(Level.TRACE, msg, *args, **kwargs)

    def dump(self, msg, *args, **kwargs):
        self.log(Level.DUMP, msg, *args, **kwargs)

    def __get_handler(self, htype:str, file_path: str or None=None):
        if file_path  is not None:
            return crate_handler(htype, file_path)

        return crate_handler(htype)

    def __set_handlers(self):
        if self.hasHandlers():
            return

        cfg = Configurator()
        file_path = cfg.get_option('log-to-file')

        handler_list = list()

        handler_list.append(LOG_TO_FILE)
        handler_list.append(LOG_TO_TEST_FILE)

        if cfg.get_option('log_to_console'):
            handler_list.append(LOG_TO_CONSOLE)

        if cfg.get_option('debug_enabled'):
            handler_list.append(LOG_TO_DEBUG_FILE)

        if cfg.get_option('trace_enabled'):
            handler_list.append(LOG_TO_TRACE_FILE)

        for htype in handler_list:
            handler = self.__get_handler(htype, file_path)
            if htype == LOG_TO_CONSOLE:
                handler.setLevel(Level.from_string(cfg.get_option('logging_level')))
            self.addHandler(handler)