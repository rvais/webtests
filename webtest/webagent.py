#!/usr/bin/env python3
#
# Framewor for testing web aplications - proof of concept 
# Authors:  Roman Vais <rvais@redhat.com>
#

import sys  # arguments accessed by  sys.argv
import os  # environment variables of the shell/machine
import errno  # errno for mkdirs function
import subprocess  # for launching another application
import logging  # python logging module
import itertools  # iteration tool of python
import re  # regex
import hashlib  # hashing algorithms for dynamic class path
import time

import pudb  # debuger

import time
# from unittest.mock import Mock

from webtest.browsers.chrome import Chrome

import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from typing import Type, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# definiton of var & const_____________________________________________

DEFAULT_LOG_LEVEL = logging.DEBUG  # CRITICAL | ERROR | WARNING | INFO | NOTSET


# definiton of functions_______________________________________________

# Class definition ____________________________________________________

class WebAgent(object):
    PROTOCOL_HTTP = "http"
    PROTOCOL_HTTPS = "https"

    BROWSER_CHROME = "chrome"
    BROWSER_FIREFOX = "firefox"

    def __init__(self):
        class_name = str(self.__class__.__name__)
        self._logger = self.__get_logger(class_name, DEFAULT_LOG_LEVEL)

        self._host = None
        self._port = None
        self._url = None
        self._protocol = None
        self._browser = None

    def __get_logger(self, name="logger", level=None, sfx=None):
        if (sfx is not None):
            name = "{}{}".format(name, sfx)

        logger = logging.getLogger(name)
        logname = "{}.log".format(name)

        # logging level for whole logger
        # can chnge log level in a subsequent call
        if (level == None):
            logger.setLevel(DEFAULT_LOG_LEVEL)

        if (not logger.hasHandlers()):
            # handler for stderr
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s]: %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(logging.ERROR) # only erros are needed
            logger.addHandler(handler)

            # handler for logging to file
            handler = logging.FileHandler(logname)
            formatter = logging.Formatter('%(asctime)s|[%(levelname)s]'
                                          ' %(name)s: %(message)s')
            handler.setFormatter(formatter)
            # logs everithing that goes to the logger
            logger.addHandler(handler)

        return logger

    def start_up_browser(self, browser: str =BROWSER_CHROME):
        if browser == WebAgent.BROWSER_CHROME:
            self._browser = Chrome()

        self._logger.debug("Launching webdriver for '{}' browser.", browser)
        self._browser.start_webdriver()

    def go_to_page(self,
            host: str,
            port: int = 0, # 8161,
            url: str = "/",
            protocol: str =PROTOCOL_HTTP):

        """

        :type port: int
        """
        self._host = host
        self._port = port
        self._url = url
        self._protocol = protocol

        url_format = '{}://{}:{}/{}'

        if len(self._url) > 0 and self._url[0] == '/':
            self._url = self._url[1:]

        if port <= 0:
            url_format = '{}://{}/{}'
            url = url_format.format(self._protocol, self._host, self._url)
        else:
            url = url_format.format(self._protocol, self._host, self._port, self._url)

        self._logger.debug("Connecting to '{}'.", url)
        self._browser.driver.get(url)

    def close_browser(self):
        self._logger.debug("Closing webbrowser.")
        self._browser.driver.quit()



# main ________________________________________________________________________
def main():
    agent = WebAgent()
    agent.start_up_browser()
    agent.go_to_page('www.google.cz')

    time.sleep(20)

    agent.close_browser()


if __name__ == '__main__':
    main()
