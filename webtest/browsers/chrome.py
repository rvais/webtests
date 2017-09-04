#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
import copy

from webtest.browsers.browser import Browser
from selenium import webdriver

class Chrome(Browser):

    def __init__(self):
        super(Chrome, self).__init__()
        self._selenium = webdriver.chrome.webdriver
        self._driver_path = 'chromedriver'
        self._browser_path = '/home/rvais/bin/chrome'

    def start_webdriver(self):
        # get default options that webdriver uses
        options = webdriver.ChromeOptions()
        options.binary_location = self._browser_path

        if self._private_mode:
            self._args.append('incognito')

        if self._maximized:
            self._args.append('start-maximized')

        # append the arguments on the list of additional arguments
        chrome_arguments = list()
        chrome_arguments.extend(self._args)
        chrome_arguments.extend(options.arguments)
        
        # filter arguments with te exclusions
        chrome_arguments = \
            list(filter(lambda x: x not in self._excludes, chrome_arguments))
        
        # put arguments back to options class/field (?)
        # options._arguments = chrome_arguments
        for arg in chrome_arguments:
            options.add_argument(arg)
        
        # start the webdriver
        self._driver = self._selenium.WebDriver(
            # chrome_options=options)
            executable_path=self._driver_path,
            chrome_options=options)

        self._driver_running = True

        return True

    def _maximize_now(self, maximize:bool=True):
        return False
