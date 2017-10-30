#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from copy import copy
from time import time, sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webtest.common.logging.logger import get_logger
from webtest.config.configurator import Configurator

class Wait(object) :

    # global profile of waiting for conditions, best known settings
    __profile__ = {
        'exception-list' : [NoSuchElementException, StaleElementReferenceException],
        'polling-period' : 2,
        'timeout' : 8,
        'max_attempts' : 3,
    }

    # config has to be implemented as if decorator was singleton
    # it allows to configure decorator globally even thou we don't have
    # references for individual decorator instances
    _config_holder = None

    def __init__(self, condition: callable): #, *args, **kwargs):
        # function to wrap
        self._condition = condition

        # configuration holder
        if Wait._config_holder is None:
            Wait._config_holder = Wait.__Wait()

        self._config = Wait._config_holder


    def __call__(self, *args, **kwargs):
        logger = self._config.logger
        logger.trace("Waiting on condition ...")
        debug_print = "Wait call\n{}"
        for x in args:
            debug_print += "\n{}"

        if kwargs and len(kwargs) > 0:
            for x in kwargs:
                if x is not None:
                    debug_print += "\n{" + x + "}"

            logger.trace(debug_print.format(self, *args, **kwargs))
        else:
            logger.trace(debug_print.format(self, *args))

        timer = time() + self._config.timeout
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
            except self._config.exception_list as ex:
                if self._config.limited and (timer <= time() or counter >= self._config.max_attempts):
                    logger.warning("All possible attempts or timer on condition "
                                         "were exhausted. Re-rising exception.")
                    raise ex

                logger.debug("Unsuccessful attempt {} to gain result. Waiting another period ...".format(counter))
                sleep(self._config.polling_period)

            except Exception as ex:
                raise ex

    @staticmethod
    def set_options(cfg: dict or Configurator):
        # configuration holder - there is no guarantee that it already exists
        if Wait._config_holder is None:
            Wait._config_holder = Wait.__Wait()

        # gain reference for config holder instance
        holder = Wait._config_holder

        # customize setting according to given configuration
        if isinstance(cfg, Configurator):
            holder.polling_period = cfg.get_option('attempt_polling_period')
            holder.timeout = cfg.get_option('attempt_timeout')
            holder.max_attempts = cfg.get_option('attempt_max_count')

        elif isinstance(cfg, dict):
            holder.polling_period = cfg['polling_period']
            holder.timeout = cfg['timeout']
            holder.max_attempts = cfg['attempt_max_count']


    # Private class serving as place holder for configuration
    class __Wait(object) :

        def __init__(self): #, *args, **kwargs):
            # setup logger
            self._class_name = str(self.__class__.__name__).strip("_")
            self._logger = None

            # accepting global profile settings
            self._exception_list = Wait.__profile__['exception-list']
            self._polling_period = Wait.__profile__['polling-period']
            self._timeout = Wait.__profile__['timeout']
            self._max = Wait.__profile__['max_attempts']

            # crete tuple of exceptions that can be used in try-except statement
            self._exceptions = tuple(self._exception_list)


        @property
        def exception_list(self) -> list:
            return copy(self._exception_list)


        @property
        def polling_period(self) -> int or float:
            return self._polling_period


        @property
        def timeout(self) -> int or float:
            return self._timeout


        @property
        def max_attempts(self) -> int:
            return self._max


        @property
        def is_limited(self) -> bool:
            return self._max >= 0 or self._timeout > 0


        @property
        def logger(self):
            if self._logger is None:
                self._logger = get_logger(self._class_name)

            return self._logger


        @polling_period.setter
        def polling_period(self, val:int or float):
            self._polling_period = val


        @timeout.setter
        def timeout(self, value:int or float):
            self._timeout = value


        @max_attempts.setter
        def max_attempts(self, value:int):
            self._max = value
