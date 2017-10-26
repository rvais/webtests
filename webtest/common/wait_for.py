#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#


from time import time, sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webtest.common.logger import get_logger
from webtest.config.configurator import Configurator

class Wait(object) :

    # global profile of waiting for conditions
    __profile__ = {
        'exception-list' : [NoSuchElementException, StaleElementReferenceException],
        'polling-period' : 2,
        'timeout' : 8,
        'max_attempts' : 3,
    }

    def __init__(self, condition: callable): #, *args, **kwargs):
        # setup logger
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        # function to wrap
        self._condition = condition

        # accepting global profile
        self._exception_list = Wait.__profile__['exception-list']
        self._polling_period = Wait.__profile__['polling-period']
        self._timeout = Wait.__profile__['timeout']
        self._max = Wait.__profile__['max_attempts']
        self._limited = self._max >= 0 or self._timeout > 0

        # log current settings
        self._logger.trace("Initialized wait conditions to following values:")
        self._logger.trace("'{}':  {}". format('exception-list', self._exception_list))
        self._logger.trace("'{}':  {}". format('polling-period', self._polling_period))
        self._logger.trace("'{}':  {}". format('timeout', self._timeout))
        self._logger.trace("'{}':  {}". format('max_attempts', self._max))

        # crete tuple of exceptions that can be used in try-except statement
        self._exceptions = tuple(self._exception_list)



    def __call__(self, *args, **kwargs):
        # customize setting according to configuration
        cfg = Configurator()
        self._polling_period = cfg.get_option('attempt_poling_period')
        self._timeout = cfg.get_option('attempt_timeout')
        self._max = cfg.get_option('attempt_max_count')
        self._limited = self._max >= 0 or self._timeout > 0

        self._logger.trace("Waiting on condition ...")
        debug_print = "Wait call\n{}"
        for x in args:
            debug_print += "\n{}"

        if kwargs and len(kwargs) > 0:
            for x in kwargs:
                if x is not None:
                    debug_print += "\n{" + x + "}"

            self._logger.trace(debug_print.format(self, *args, **kwargs))
        else:
            self._logger.trace(debug_print.format(self, *args))

        timer = time() + self._timeout
        counter = 0
        while True:
            counter += 1
            try:
                arg_tuple = args
                result = self._condition(*arg_tuple, **kwargs)
                # if (result and self._expected) or (not result and not self._expected):
                return result
                # else:
                #    self._logger.warning("Condition on result failed. Waiting another period ...")
            except self._exceptions as ex:
                if self._limited and (timer <= time() or counter >= self._max):
                    self._logger.warning("All possible attempts or timer on condition "
                                         "were exhausted. Re-rising exception.")
                    raise ex

                self._logger.debug("Unsuccessful attempt {} to gain result. Waiting another period ...".format(counter))
                sleep(self._polling_period)

            except Exception as ex:
                raise ex

