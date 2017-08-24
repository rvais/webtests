#!/usr/bin/env python3
#
# Framewor for testing web aplications - proof of concept 
# Authors:  Roman Vais <rvais@redhat.com>
#
import copy
from selenium.webdriver.firefox import webdriver

from webtest.browsers.browser import Browser
from selenium import webdriver

class Firefox(Browser):

    def __init__(self):
        super(Firefox, self).__init__()
        self._selenium = None
        self._driver_path = 'geckodriver'
        self._browser_path = '/usr/bin/firefox'

    def start_webdriver(self):
        firefox_options = webdriver.firefox.webdriver.Options()
        
        
        if self._private_mode:
            self._args.append('incognito')

        # append the arguments on the list of additional arguments
        firefox_arguments = list()
        firefox_arguments.extend(self._args)
        firefox_arguments.extend(firefox_options.arguments)
        
        # filter arguments with te exclusions
        firefox_arguments = \
            list(filter(lambda x: x not in self._excludes, firefox_arguments))
        
        # put arguments back to options class/field (?)
        firefox_options._arguments = firefox_arguments
        # for arg in firefox_arguments:
        #     options.add_argument(arg)
        
        # start the webdriver
        self._driver = webdriver.Firefox(firefox_binary=self._browser_path,
            executable_path=self._driver_path, firefox_options=firefox_options)

        return self._driver
