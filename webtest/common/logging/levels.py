#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
import logging  # python logging module

class Level(object):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    TRACE = 5
    DUMP = 1
    NOTSET = logging.NOTSET
    DEFAULT = logging.INFO

    __mapping_dictionary = {
        "CRITICAL" : CRITICAL,
        "ERROR" : ERROR,
        "WARNING" : WARNING,
        "INFO" : INFO,
        "DEBUG" : DEBUG,
        "TRACE" : TRACE,
        "DUMP" : DUMP,
        "NOTSET" : NOTSET,
        "DEFAULT" : INFO,
    }

    @staticmethod
    def from_string(level:str) -> int:
        value = None
        try:
            value = Level.__mapping_dictionary[level]
        except Exception:
            pass

        return value if value is not None else Level.DEFAULT

    @staticmethod
    def setup_logging_levels(self):
        logging.addLevelName(Level.TRACE, "TRACE")
        logging.TRACE = Level.TRACE
        logging.addLevelName(Level.DUMP, "DUMP")
        logging.DUMP = Level.DUMP
