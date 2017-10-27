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

        # browser name
        choices = [WebAgent.BROWSER_CHROME, WebAgent.BROWSER_FIREFOX]
        kwargs = {
            'action'  : 'store',
            'nargs'   : '?',
            'default' : WebAgent.BROWSER_CHROME,
            'choices' : choices,
            'help'    : 'Name of the web browser to be used in testing. Supported are following:'
                        '\n"{choices}"'.format(choices='", "'.join(choices)),
            'metavar' : 'BROWSER_NAME',
        }
        self._delegate.add_argument('--browser', '-b', **kwargs)

        # path to browser binary
        kwargs = {
            'action' : 'store',
            'nargs'  : '?',
            'help'   : 'If path to binary of your browser is not standard one,'
                       ' or there is an issue with locating the browser,'
                       ' use this option to provide correct path.',
        }
        self._delegate.add_argument('--browser-bin-path', '-r', **kwargs)

        # path to webdriver binary
        kwargs = {
            'action' : 'store',
            'nargs'  : '?',
            'help'   : 'If path to binary of web driver for selected browser is '
                       'not standard one, or there is an issue with locating the'
                       ' browser, use this option to provide correct path.',
        }
        self._delegate.add_argument('--driver-bin-path', '-d', **kwargs)

        # path to configuration file
        kwargs = {
            'action': 'store',
            'nargs' : '?',
            'help'  : 'Path to configuration fail containing presets for this test-suit.',
        }
        self._delegate.add_argument('--config-file', '-g', **kwargs)

        # logging level
        choices = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'DUMP', 'NOTSET', 'DEFAULT']
        kwargs = {
            'action'  : 'store',
            'nargs'   : '?',
            'default' : 'DEFAULT',
            'choices' : choices,
            'help'    : 'Capitalized name of logging level to provide. Supported are following values:'
                        '\n{choices}'.format(choices=', '.join(choices)),
            'metavar' : 'LEVEL',
        }
        self._delegate.add_argument('--logging-level', '-l', **kwargs)

        # disable console output
        kwargs = {
            'action' : 'store_false',
            'help'   : 'Disables console output so logging (if any) will be only into file.',
        }
        self._delegate.add_argument('--logging-to-console-disabled', **kwargs)

        # log file name
        kwargs = {
            'action' : 'store',
            'nargs'  : '?',
            'help'   : 'Changes file name to store logs form current run into.',
        }
        self._delegate.add_argument('--log-to-file', '-f', **kwargs)

        # enable extra debug log file
        kwargs = {
            'action' : 'store_true',
            'help'   : 'Enables DEBUG level logging output to extra file, regardless of logging level'
                       ' that is set. Other outputs will comply with logging level.',
        }
        self._delegate.add_argument('--debug-enabled', **kwargs)

        # enable extra trace log file
        kwargs = {
            'action' : 'store_true',
            'help'   : 'Enables TRACE level logging output to extra file, regardless of logging level'
                       ' that is set. Other outputs will comply with logging level.',
        }
        self._delegate.add_argument('--trace-enabled', **kwargs)

        # path to python package with scenarios
        default_path = './tests/scenarios/'
        kwargs = {
            'action'  : 'store',
            'nargs'   : '?',
            'default' : default_path,
            'help'    : 'Path to python package with preset scenarios to run.'
                        ' Default value is: {path}'.format(path=default_path),
        }
        self._delegate.add_argument('--scenarios-path', **kwargs)

        # scenario class
        kwargs = {
            'action'   : 'store',
            'nargs'    : '?',
            'help'     : 'Name of scenario class (i.e. subset, subdir) that will be used '
                         'to search individual scenarios.',
            'required' : True,
        }
        self._delegate.add_argument('--scenarios-class', '-c', **kwargs)

        # scenario name
        kwargs = {
            'action'   : 'store',
            'nargs'    : '+',
            'help'     : 'Name of individual scenarios from given class that should be run/executed.',
            'required' : True,
        }
        self._delegate.add_argument('--execute-scenarios', '-e', **kwargs)

        # screenshot policy
        choices = ['each_action', 'on_failure', 'disabled']
        kwargs = {
            'action'  : 'store',
            'nargs'   : '?',
            'default' : 'disabled',
            'choices' : choices,
            'help'    : 'Option specifies if and when should screenshots be taken.'
                        ' Supported values are following:'
                        '\n"{choices}"'.format(choices='", "'.join(choices)),
            'metavar' : 'POLICY',
        }
        self._delegate.add_argument('--screenshots', '-s', **kwargs)


    def parse_arguments(self, args) -> dict:
        namespace = vars(self._delegate.parse_args(args))
        options = dict()

        for option, value in namespace.items():
            if option in ArgumentParser.translation.keys():
                option = ArgumentParser.translation[option]
            options[option] = value

        return options