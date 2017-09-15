#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import logging


from webtest.common.logger import get_logger
from webtest.webagent import WebAgent


class MouseAction(object):
    def __init__(self):
        self._class_name = str(self.__class__.__name__)
        self._logger = get_logger(self._class_name) # type: logging.Logger

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Performing mouse action.")
        return True

    def action_failure(self, ex: Exception=None, msg: str=None ):
        self._logger.info("Action '{}' FAILED.".format(self._class_name))
        if msg is not None:
            self._logger.info(msg)

        if ex is not None:
            self._logger.warning(ex)