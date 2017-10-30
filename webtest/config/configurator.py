#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import os  # environment variables of the shell/machine

from configparser import ConfigParser

_section_name = "Basic"

# Singleton/SingletonPattern.py
class Configurator(object):
    _instance = None

    def __init__(self, config_file: str=None, *arg, **kwords):


        if Configurator._instance is None:
            cf = config_file
            if cf is None:
                cf = "./webtest.cfg"

            Configurator._instance = Configurator.__ConfiguratorImpl(cf, *arg, **kwords)

        self._delegate = Configurator._instance
        if config_file is not None:
            self._delegate.update_from_file(config_file)

    def get_option(self, name: str):
        return Configurator.process_value(self._delegate.get_option(name))

    def set_option(self, name: str, value: object):
        self._delegate.set_option(name, value)

    def set_multiple_options(self, options:dict):
        for key, value in options.items(): # type: str
            if value is None:
                continue

            self.set_option(key, value)

    def save_as(self, file_name: str):
        self._delegate.save_as(file_name)

    @staticmethod
    def process_value(option: str) -> str or int or bool:
        boolean_strings = ['True', 'true', 'TRUE', 'False', 'false', 'FALSE']

        if isinstance(option, str):
            option = option.strip('"')
            try:
                i = boolean_strings.index(option)
                if i < 3:
                    return True
                else:
                    return False

            except ValueError as ex:
                pass

            try:
                if option.index('.') >= 0:
                    return float(option)

            except ValueError as ex:
                pass

            try:
                return int(option)

            except ValueError as ex:
                pass

        return option



    class __ConfiguratorImpl(object):
        def __init__(self, config_file, *arg, **kwords):
            defaults = {
                _section_name : {
                    'browser' : 'chrome',
                    'browser_bin_path' : 'google-chrome',
                    'driver_bin_path' : 'chromedriver',
                    'logging_level' : 'DEFAULT',
                    'log_to_console' : True,
                    'debug_enabled' : True,
                    'trace_enabled' : True,
                    'scenarios_path' : './tests/scenarios/',
                    'attempt_polling_period' : 2,
                    'attempt_timeout' : 8,
                    'attempt_max_count' : 3,
                }
            }

            environmental_variables = {
                'browser_bin_path' : 'BROWSER_BIN_PATH',
                'driver_bin_path' : 'DRIVER_BIN_PATH',
            }

            print("Inicializing configuration ...")
            self.additional = dict()
            self.cfg = ConfigParser(empty_lines_in_values=False)
            self.cfg.optionxform = str
            self.cfg.read_dict(defaults)
            if os.path.exists(config_file) and os.path.isfile(config_file):
                print("Configuration file '{}' does exist.".format(config_file))
                try:
                    self.cfg.read_file(open(config_file))
                except BaseException as ex:
                    print("Cannot parse configuration file. Falling back to default settings.")

            else:
                print("Configuration file does not exist, falling back to default settings.")
                print("Storing configuration to given file.")
                with open(config_file,'w') as file:
                    self.cfg.write(file)

            for option, variable in environmental_variables.items():
                if variable in os.environ.keys():
                    value = os.environ[variable]
                    # self._logger.debug("Environment variable '{}' has been set to value '{}'.".format(variable, value))
                    print("Environment variable '{}' has been set to value '{}'.".format(variable, value))
                    self.cfg.set(_section_name, option, value)
                    if self.cfg.get(_section_name, option, raw=True) != value:
                        raise Exception("Attempt to set new value was not successful.")

        def get_option(self, name:str, section: str=_section_name) -> str or None:
            if self.cfg.has_option(section, name):
                return self.cfg.get(section, name, raw=True)

            if name in self.additional.keys():
                return self.additional[name]

            return None

        def set_option(self, name: str, value: object):
            if not isinstance(value, str):
                if isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
                    value = str(value)

                else:
                    if self.cfg.has_option(_section_name, name):
                        self.cfg.remove_option(_section_name, name)

                    self.additional[name] = value
                    return

            self.cfg.set(_section_name, name, value)
            if self.cfg.get(_section_name, name, raw=True) != value:
                raise Exception("Attempt to set new value was not successful.")

            return

        def save_as(self, file_name:str):
            with open(file_name, 'w') as file:
                self.cfg.write(file)


        def update_from_file(self, config_file:str):
            if os.path.exists(config_file) and os.path.isfile(config_file):
                print("Configuration file '{}' does exist.".format(config_file))
                try:
                    self.cfg.read_file(open(config_file))
                except BaseException as ex:
                    print("Cannot parse configuration file. Falling back to previous settings.")