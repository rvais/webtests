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

from webtest.browsers.browser import Browser
from webtest.browsers.chrome import Chrome
from webtest.common.logger import get_logger
from webtest.common.http import Constants as HTTP_CONST
from webtest.components.models.google.google import GoogleMainPage
from webtest.components.pagemodel import model
from webtest.components.pagemodel.model import PageModel
from webtest.components.pagemodel.page import Page

# import pytest
# from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
# from typing import Type, List

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# definition of var & const_____________________________________________

# definition of functions_______________________________________________

# Class definition ____________________________________________________

class WebAgent(object):
    BROWSER_CHROME = "chrome"
    BROWSER_FIREFOX = "firefox"

    BROWSER_PATH = None
    DRIVER_PATH = None

    def __init__(self):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._host = None
        self._port = None
        self._url = None
        self._protocol = None
        self._browser = None
        self._page = None

    def start_up_browser(self, browser: str =BROWSER_CHROME):
        if browser == WebAgent.BROWSER_CHROME:
            self._browser = Chrome()
        
        self._logger.debug("'{}' has been selected as browser.".format(browser))

        envvar = "BROWSER_BIN_PATH"
        if envvar in os.environ:
            self._logger.debug("Environment variable '{}' has been set.".format(envvar))
            self._logger.debug("Path '{}' has been set as binary for '{}' browser."
                .format(os.environ[envvar], browser))
            self._browser.set_new_browser_path(os.environ[envvar])

        envvar = "DRIVER_BIN_PATH"
        if envvar in os.environ:
            self._logger.debug("Environment variable '{}' has been set.".format(envvar))
            self._logger.debug("Path '{}' has been set as binary"
                " for selenium webdriver.".format(os.environ[envvar]))
            self._browser.set_new_webdriver_path(os.environ[envvar])


        self._logger.debug("Launching webdriver for '{}' browser.".format(browser))
        self._browser.start_webdriver()

    def go_to_page(self,
            host: str,
            port: int = 0, # 8161,
            url: str = "/",
            protocol: str =HTTP_CONST.PROTOCOL_HTTP):

        self._logger.debug("Creating new page model without any components.")
        model = PageModel(protocol=protocol, host=host, port=port, url=url)

        self._logger.debug("Connecting to '{}' via this address.".format(model.url))
        return self.get_page(model=model)

    def get_page(self, model: PageModel=None, full_url: str=None):
        if model is not None:
            debug_message = "Getting page '{}' based on predefined model/template."
            self._logger.debug(debug_message.format(model.url))
            return self._browser.get_page(model=model)
        elif full_url is not None and len(full_url) > 0:
            debug_message = "Getting page '{}' based on url only."
            self._logger.debug(debug_message.format(model.url))
            return self._browser.get_page(model=model)
        else:
            self._logger.warning("No page template or url has been supplied to get_page() method.")
            return None


    def close_browser(self):
        self._logger.debug("Closing webbrowser.")
        self._browser.quit()



# main ________________________________________________________________________
def main():
    agent = WebAgent()

    agent.start_up_browser()
    agent.get_page(GoogleMainPage())
    time.sleep(5)
    agent.close_browser()

    agent.start_up_browser()
    agent.go_to_page("www.google.cz")
    time.sleep(5)
    agent.close_browser()


if __name__ == '__main__':
    main()
