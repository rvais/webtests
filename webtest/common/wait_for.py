#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import time, sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webtest.common.logger import get_logger

# EC.url_changes
# EC.element_located_to_be_selected
# EC.alert_is_present
# EC.frame_to_be_available_and_switch_to_it
# EC.presence_of_all_elements_located
# EC.presence_of_element_located
# EC.text_to_be_present_in_element
# EC.text_to_be_present_in_element_value

#WebDriverWait(ff, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))

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

        # customize setting according to parameters
        # self._setup(*args, **kwargs)

        # log current settings
        self._logger.trace("Initialized wait conditions to following values:")
        self._logger.trace("'{}':  {}". format('exception-list', self._exception_list))
        self._logger.trace("'{}':  {}". format('polling-period', self._polling_period))
        self._logger.trace("'{}':  {}". format('timeout', self._timeout))
        self._logger.trace("'{}':  {}". format('max_attempts', self._max))

        # crete tuple of exceptions that can be used in try-except statement
        self._exceptions = tuple(self._exception_list)


#    def _setup(self, expected_result: bool=True, timeout: int=-1, polling_period: float=-1.0,
#                 max_attempts: int=-1, exception_list: list=list()):
#        self._logger.debug("Setting up custom values ...")
#        self._expected = expected_result
#
#        if timeout >= 0:
#           self._timeout = timeout
#
#        if polling_period > 0:
#            self._polling_period = polling_period
#
#        if max_attempts > 0:
#            self._max = max_attempts
#
#        self._exception_list.extend(exception_list)


    def __call__(self, *args, **kwargs):
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



    @staticmethod
    def set_wait_condition_profile(profile: dict) -> bool :
        class_name = str(__class__.__name__)
        logger = get_logger(class_name)
        logger.debug("Setting up global waiting profile.")

        check = False
        for key in Wait.__profile__:
            if key in profile.keys():
                check = True
                Wait.__profile__[key] = profile[key]
        return check
