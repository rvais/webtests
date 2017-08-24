#!/usr/bin/env python3
#
# Framewor for testing web aplications - proof of concept 
# Authors:  Roman Vais <rvais@redhat.com>
#
from selenium import webdriver

class Browser(object):

    def __init__(self):
        self._selenium = None
        self._driver = None
        self._driver_path = ''
        self._browser_path = ''
        self._private_mode = False
        self._args = list()
        self._excludes = list()

    @property
    def driver(self):
        return self._driver

    @property
    def path_to_driver(self):
        return self._driver_path
    
    @property
    def path_to_browser(self):
        return self._browser_path

    def set_cmd_arguments(self, args: list):
        self._args = args

    def exclude_cmd_arguments(self, args: list):
        self._excludes = args

    def add_cmd_arguments(self, args: list):
        self._args.extend(args)

    def exclude_aditional_cmd_arguments(self, args: list):
        self._excludes.extend(args)

    def add_cmd_argument(self, arg: str):
        self._args.append(arg)

    def exclude_aditional_cmd_argument(self, arg: list):
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


    def set_path_to_default(self):
        self._path = ''

    def use_private_mode(self, private: bool =True):
        original = self._private_mode
        self._private_mode = private
        return original

    def start_webdriver(self):
        raise Exception('Browser is "abstract" class and method'
            ' "start_webdriver()" needs to be implemented in subclasses.')



