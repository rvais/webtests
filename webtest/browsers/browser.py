#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from selenium.webdriver.remote.webdriver import WebDriver
from webtest.browsers.mockdriver import MockDriver
from webtest.components.pagemodel.model import PageModel
from webtest.components.pagemodel.page import Page
from webtest.common.wait_for import Wait
from webtest.common.http import URL
from webtest.common.logging.logger import get_logger

class Browser(object):

    def __init__(self):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._selenium = None
        self._driver = MockDriver() # type:WebDriver
        self._driver_path = ''
        self._browser_path = ''
        self._private_mode = False
        self._maximized = True
        self._args = list()
        self._excludes = list()
        self._current_page = None
        self._driver_running = False

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def path_to_driver(self) -> str:
        return self._driver_path
    
    @property
    def path_to_browser(self) -> str:
        return self._browser_path

    @property
    def is_running(self) -> bool:
        return self._driver_running

    def set_cmd_arguments(self, args: list):
        self._args = args

    def exclude_cmd_arguments(self, args: list):
        self._excludes = args

    def add_cmd_arguments(self, args: list):
        self._args.extend(args)

    def exclude_additional_cmd_arguments(self, args: list):
        self._excludes.extend(args)

    def add_cmd_argument(self, arg: str):
        self._args.append(arg)

    def exclude_additional_cmd_argument(self, arg: list):
        self._excludes.append(arg)

    def set_new_webdriver_path(self, path: str):
        if len(path) <= 0:
            raise \
                Exception("Attempt to set empty path for a Browser webdriver.")
        else:
            self._driver_path = path

    def set_new_browser_path(self, path: str):
        if len(path) <= 0:
            raise \
                Exception("Attempt to set empty path for a web browser.")
        else:
            self._browser_path = path

    def use_private_mode(self, private: bool =True) -> bool:
        original = self._private_mode
        self._private_mode = private
        return original

    def maximize(self, maximize:bool=True) -> bool:
        if self.is_running:
            return self._maximize_now()

        self._maximized = maximize
        return True

    def _maximize_now(self, maximize:bool=True):
        return False

    def start_webdriver(self):
        raise Exception('Browser is "abstract" class and method'
            ' "start_webdriver()" needs to be implemented in subclasses.')

    def quit(self):
        self._logger.debug("Browser exiting.")
        self._driver.quit()
        self._driver_running = False

    def get_page(self, full_url:str =None, model: PageModel=None, update: bool=False) -> Page:

        if full_url is not None and len(full_url) > 0:
            self._logger.debug("Browser has URL available.")
            self._driver.get(full_url)
            self._current_page = Page(self)

        elif model is not None:
            self._logger.debug("Browser has Page Model available.")
            if not update:
                self._driver.get(model.url.string(True, True))

            if not self.current_url.is_similar_to(model.url):
                self._logger.warning("Current browser's url and template's url do not match.")
                msg = "browser's url:\n\t\t'{}'\n\ttemplate's url:\n\t\t'{}'"
                self._logger.warning(msg.format(self.current_url, model.url))

            self._current_page = Page(self, model)

        return self._current_page

    @property
    def get_current_page(self) -> Page:
        return self._current_page

    @property
    def current_url(self) -> URL:
        return URL.parse(self.driver.current_url)

    @Wait
    def inject_script(self, script: str, async: bool=True) -> object:
        self._driver.set_script_timeout(10)
        if async:
            result = self._driver.execute_async_script(script)
        else:
            result = self._driver.execute_script(script)

        return result