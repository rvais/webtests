#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
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

import pudb  # debuger

from time import sleep
# from unittest.mock import Mock
# from webtest.actions.user_action import UserAction
# from webtest.browsers.browser import Browser
from webtest.browsers.chrome import Chrome
from webtest.common.logger import get_logger
from webtest.common.http import Constants as HTTP_CONST, relax_url, cut_host_from_url
from webtest.components.models.google.google import GoogleMainPage
from webtest.components.models.hawtio.LoginPage import HawtioLoginPageNS
from webtest.components.pagemodel import model
from webtest.components.pagemodel.model import PageModel
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.component import Component

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

    def __init__(self, template_list: list=list()):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._browser = None # type: Browser
        self._page = None
        self._templates_by_url = dict()
        self._templates_by_name = dict()

        for template in template_list: # type: PageModel
            self._templates_by_url[template.url] = template
            self._templates_by_name[template.name] = template

    def start_up_browser(self, browser: str =BROWSER_CHROME) -> None:
        if self._browser is not None and self._browser.name.lower() == browser:
            if self._browser.is_running:
                self._logger.debug("Selected browser is already running.")
                return
            else:
                self._logger.debug("Starting up already existing instance of browser.")
                self._browser.start_webdriver()
                return

        elif self._browser is not None and self._browser.is_running:
            self._logger.debug("Exchanging browser instances.")
            self._browser.quit()

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
        return

    def close_browser(self) -> None:
        self._logger.debug("Closing webbrowser.")
        self._browser.quit()
        return

    def is_browser_running(self):
        if self._browser is not None:
            return self._browser.is_running

        return False

    def go_to_page(self,
            host: str,
            port: int = 0, # 8161,
            url: str = "/",
            protocol: str =HTTP_CONST.PROTOCOL_HTTP) -> Page or None:

        self._logger.debug("Creating new page model without any components.")
        model = PageModel(protocol=protocol, host=host, port=port, url=url)

        self._logger.debug("Connecting to '{}' via this address.".format(model.url))
        return self.get_page(page_model=model)

    def get_page(self, page_model: PageModel=None, full_url: str=None, name=None) -> Page or None:
        if page_model is not None:
            debug_message = "Getting page '{}' based on predefined model/template."
            self._logger.debug(debug_message.format(page_model.url))

        elif full_url is not None and len(full_url) > 0:
            debug_message = "Getting page '{}' based on url."
            self._logger.debug(debug_message.format(full_url))

            if full_url not in self._templates_by_url.keys():
                page_model = Page(self._browser)
                self._logger.warning("No page template been supplied for given url.")
            else:
                self._logger.info("Page model found for given url.")
                page_model = self._templates_by_url[full_url]

        elif name is not None and name in self._templates_by_name.keys():
            self._logger.info("Page model found for given name.")
            page_model = self._templates_by_name[name]
        else:
            self._logger.error("No page template or url has been supplied to get_page() method.")
            page = None

        if page_model is not None:
            page = self._browser.get_page(model=page_model)

        return page

    def get_current_page(self) -> Page or None:
        return self._browser.get_current_page

    def perform_action(self, action: 'UserAction') -> bool:
        success = action.perform_self(self)
        waited = False
        if action.expected_redirection():
            waited = True
            action.wait_for_frameworks(self)

            url = relax_url(self._browser.current_url)

            if url in self._templates_by_url.keys():
                model = self._templates_by_url[url]
            else:
                self._logger.debug(str(self._templates_by_url.keys()))
                self._logger.debug(url)

                h = hashlib.sha256()
                current_model = self._browser.get_current_page.model

                h.update(current_model.name.encode('utf-8'))
                h.update(current_model.url.encode('utf-8'))
                h.update(url.encode('utf-8'))

                name = "{}-{}".format(current_model.name, h.hexdigest())

                model = current_model.derive_template(name, url=cut_host_from_url(url))
                self._templates_by_url[url] = model
                self._templates_by_name[name] = model

            self._browser.get_page(model=model, update=True)

        if action.expected_content_change() and not waited:
            action.wait_for_frameworks(self)

        if action.delay_for_user_to_see():
            sleep(5)

        return success

    def perform_action_get(self, action: 'UserAction') -> object or None:
        return action.perform_self(self)


# main ________________________________________________________________________
def main():
    pass


if __name__ == '__main__':
    main()
