#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from argparse import ArgumentParser as AP
from webtest.webagent import WebAgent

class ArgumentParser(object):
    translation = {
        'logging_to_console_disabled' : 'log_to_console'
    }
    def __init__(self):
        self._delegate = AP(description="Test suite for web based applications.")
        #(name, action, count of arguments, None, default value, type, [list of choices], required=True)
        self._delegate.add_argument('--browser', '-b', action='store', nargs='?', default=WebAgent.BROWSER_CHROME,
                                    choices=[WebAgent.BROWSER_CHROME, WebAgent.BROWSER_FIREFOX]) # browser
        self._delegate.add_argument('--browser-bin-path', '-r', action='store', nargs='?') # browser path
        self._delegate.add_argument('--driver-bin-path', '-d', action='store', nargs='?') # driver path
        self._delegate.add_argument('--config-file', '-g', action='store', nargs='?') # driver path
        self._delegate.add_argument('--logging-level', '-l', action='store', nargs='?', default='DEFAULT',
                                    choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'DUMP', 'NOTSET', 'DEFAULT']) # log level
        self._delegate.add_argument('--logging-to-console-disabled', action='store_false') # log to console
        self._delegate.add_argument('--log-to-file', '-f', action='store', nargs='?') # log to file
        self._delegate.add_argument('--debug-enabled', action='store_true') # log debug
        self._delegate.add_argument('--trace-enabled', action='store_true') # log trace
        self._delegate.add_argument('--scenarios-path', action='store', nargs='?', default='./tests/scenarios/') # replacement path to package with scenarios
        self._delegate.add_argument('--scenarios-class', '-c', action='store', nargs='?',default='', required=True) # scenarios directory
        self._delegate.add_argument('--execute-scenarios', '-e', action='store', nargs='+', required=True) # scenarios to execute
        self._delegate.add_argument('--screenshots', '-s', action='store', nargs='?', default='disabled',
                                    choices=['each_action', 'on_failure', 'disabled']) # screenshot [each_action, on_failure, disabled]


    def parse_arguments(self, args) -> dict:
        namespace = vars(self._delegate.parse_args(args))
        options = dict()

        for option, value in namespace.items():
            if option in ArgumentParser.translation.keys():
                option = ArgumentParser.translation[option]
            options[option] = value

        return options