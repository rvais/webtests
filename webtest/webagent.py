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
from webtest.common.logging.logger import get_logger
from webtest.common.http import Constants as HTTP_CONST, relax_url, cut_host_from_url
from webtest.common.http import URL
from webtest.components.models.google.google import GoogleMainPage
from webtest.components.models.hawtio.login_page import HawtioLoginPageNS
from webtest.components.pagemodel import model
from webtest.components.pagemodel.model import PageModel
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.component import Component
from webtest.config.configurator import Configurator

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

#
# WebAgent class is supposed to represent user of the website and store
# resources available to such user. This includes Templates of potentially
# visited webpages (i.e. knowledge about these pages) and browser it self.
# Class has method to perform given user actions in browser and by doing
# so simulate user's behavior.
#
class WebAgent(object):
    BROWSER_CHROME = "chrome"
    BROWSER_FIREFOX = "firefox"

    BROWSER_PATH = None
    DRIVER_PATH = None

    def __init__(self, template_list: list=list(), browser_path: str or None=BROWSER_PATH, driver_path: str or None=DRIVER_PATH):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._browser = None # type: Browser
        self._page = None

        self._templates_by_url = dict()
        self._templates_by_name = dict()
        self.add_more_templates(template_list)
        self._browser_path = browser_path
        self._driver_path = driver_path

    #
    # Method is supposed to replace existing templates with new set.
    # @param template_list: list of instances inherited form PageModel
    # @return None
    #
    def refresh_templates(self, template_list: list=list()) -> None:
        self._logger.info("Clearing up page templates.")
        self._templates_by_url = dict()
        self._templates_by_name = dict()

        self.add_more_templates(template_list)


    #
    # Method is supposed to add to existing templates collection new ones.
    # @param template_list: list of instances inherited form PageModel
    # @return None
    #
    def add_more_templates(self, template_list: list=list()) -> None:
        self._logger.info("Adding {} new page templates.".format(len(template_list)))
        for template in template_list: # type: PageModel
            self._templates_by_url[template.url.string()] = template
            self._templates_by_name[template.name] = template


    #
    # Method starts instance of selected web browser. Default one is
    # google chrome. If there is already running browser under this
    # instance of WebAgent and replacement is different browser,
    # current instance is closed and replacement is started.
    # @param browser: name of web browser to use
    # @return None
    #
    def start_up_browser(self, browser: str =None) -> None:
        cfg = Configurator()
        if browser is None:
            browser = cfg.get_option('browser')

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

#        if browser == WebAgent.BROWSER_FIREFOX:
#            self._browser = Firefox()
        
        self._logger.debug("'{}' has been selected as browser.".format(browser))

        browser_path = self._browser_path
        driver_path = self._driver_path

        if browser_path is None:
            browser_path = cfg.get_option('browser_bin_path')
            self._logger.debug("Path '{}' has been set as binary for '{}' browser."
                .format(browser_path, browser))

        if driver_path is None:
            driver_path = cfg.get_option('driver_bin_path')
            self._logger.debug("Path '{}' has been set as binary" 
                " for selenium webdriver.".format(driver_path))

        self._browser.set_new_browser_path(browser_path)
        self._browser.set_new_webdriver_path(driver_path)

        self._logger.debug("Launching webdriver for '{}' browser.".format(browser))
        self._browser.start_webdriver()
        return


    #
    # Method closes instance of selected web browser. Default one is google chrome.
    # @param browser: name of web browser to use
    # @return None
    #
    def close_browser(self) -> None:
        self._logger.debug("Closing webbrowser.")
        self._browser.quit()
        return


    #
    # Method returns information about state of browser under this instance of WebAgent
    # @return True if some instance of browser is running, False otherwise
    #
    def is_browser_running(self) -> bool:
        if self._browser is not None:
            return self._browser.is_running

        return False


    #
    # Method makes the running browser to visit page with use of URL.
    #
    # @param host: hostname that is part of URL (e.g. www.example.com or IP address)
    # @param port: port number in case it is not standard port 80
    #              value 0 means not uo use port number in URL
    # @param uri: string that is usually part of HTTP GET request
    # @param protocol: in some cases called schema - "http" or "https"
    # @return instance of Page
    #
    def go_to_page(self,
            host: str,
            port: int = 0, # 8161,
            uri: str = "/",
            protocol: str =HTTP_CONST.PROTOCOL_HTTP) -> Page or None:

        self._logger.debug("Creating new page model without any components.")
        model = PageModel(protocol=protocol, host=host, port=port, uri=uri)

        self._logger.debug("Connecting to '{}' via this address.".format(model.url))
        return self.get_page(page_model=model)


    #
    # Method makes the running browser to visit page with use one of the methods represented
    # by its arguments. User is supposed to fill only one of them.
    #
    # @param page_model: PageModel instance containing template and URL for page to visit
    # @param full_url: full URL address as it can be seen in browsers address bar
    # @param name: name of the template known to this instance of WebAgent
    # @return instance of Page
    #
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


    #
    # Method returns instance of web page currently displayed in browser assuming
    # that only this instance of WebAgent was interacting with it. Otherwise
    # method returns instance of web page that is last known visited page by this
    # instance of WebAgent.
    #
    # @param None
    # @return instance of Page
    #
    def get_current_page(self) -> Page or None:
        return self._browser.get_current_page


    #
    # Method performs action represented by object given to it as argument as if
    # it is action performed by actual user browsing the internet.
    #
    # @param action: instance of UserAction or its subclasses
    # @return True if action succeeded, False otherwise
    #
    def perform_action(self, action: 'UserAction') -> bool:
        success = action.perform_self(self)
        # It is not necessary to wait for frameworks twice #0
        waited = False

        if action.expected_redirection():
            # It is not necessary to wait for frameworks twice #1
            waited = True

            # there is minimal time required for browser to even change
            # urls and propagate them to selenium
            sleep(1)

            # remove anchors and HTTP GET method variables
            # otherwise we would have to create infinite number of templates/models
            url = self._browser.current_url # type: URL

            # get template/model or derive it by cloning current one
            if url.string() in self._templates_by_url.keys():
                model = self._templates_by_url[url.string()]
            else:
                self._logger.debug(str(self._templates_by_url.keys()))
                self._logger.debug(url)

                # make hash so new template can be stored and later identified by the same url or name
                # but does not override any of the current templates
                h = hashlib.sha256()
                current_model = self._browser.get_current_page.model

                h.update(current_model.name.encode('utf-8'))
                h.update(current_model.url.encode('utf-8'))
                h.update(url.encode('utf-8'))

                # new name incorporates the hash
                name = "{}-{}".format(current_model.name, h.hexdigest())

                model = current_model.derive_template(name, uri=url.uri)
                self._templates_by_url[url] = model
                self._templates_by_name[name] = model

            # get new page that has corresponding template
            page = self._browser.get_page(model=model, update=True)
            page.construct_page()

            # wait for frameworks to recreate page elements in browser
            action.wait_for_frameworks(self)

        # It is not necessary to wait for frameworks twice #2
        if action.expected_content_change() and not waited:
            action.wait_for_frameworks(self)

        if action.delay_for_user_to_see() > 0:
            sleep(action.delay_for_user_to_see())

        return success


    #
    # Experimental method that performs action represented by object given
    # to it as argument as if it is action performed by actual user browsing
    # the internet. Unlike perform_action method it is supposed to return
    # actual result of given action. Result depends on action implementation
    # of action object it self and not on this method.
    #
    # @param action: instance of UserAction or its subclasses
    # @return True if action succeeded, False otherwise
    #
    def perform_action_get(self, action: 'UserAction') -> object or None:
        return action.perform_self(self)


# main ________________________________________________________________________
def main():
    pass


if __name__ == '__main__':
    main()
