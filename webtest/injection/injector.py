#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
import copy

class Injector(object):
    _instance = None

    def __init__(self, config_file: str=None, *args, **kwargs):

        if Configurator._instance is None:
            cf = config_file
            if cf is None:
                cf = "./webtest.cfg"

            Configurator._instance = Configurator.__ConfiguratorImpl(cf, *args, **kwargs)

    @staticmethod
    def getInstance(clazz: type, *args, **kwargs):
        return clazz(*args, **kwargs)

    class __InjectorImpl(object):
        def __init__(self, *args, **kwargs):
            pass

        def method(self, *args, **kwargs) -> None:
            pass

