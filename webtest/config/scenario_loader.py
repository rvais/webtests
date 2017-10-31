#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import os


try:
    from pkgutil import walk_packages
except ImportError as ex:
    raise ex


# Singleton/SingletonPattern.py
class ScenarioLoader(object):
    _instance = None

    def __init__(self, *arg, **kwords):
        if ScenarioLoader._instance is None:
            ScenarioLoader._instance = ScenarioLoader.__ScenarioLoaderImpl(*arg, **kwords)

        self._delegate = ScenarioLoader._instance

    def load_scenario(self, group_name: str, scenario_name: str) -> tuple or None:
        return self._delegate.load_scenario(group_name, scenario_name)

    def add_scenario(self, group_name: str, scenario_name: str, importer: object, module_name: str):
        self._delegate.add_scenario(group_name, scenario_name, importer, module_name)

    # walk through given path and import all available submodules
    def add_all_scenarios(self, paths: str or list, parent: str=""):
        if isinstance(paths, str):
            paths = [paths, ]

        subpaths = list()

        for loader, module_name, is_pkg in walk_packages(paths):
            if is_pkg:
                subpath = os.path.join(loader.path, module_name)
                following = (subpath, os.path.join(parent, module_name))
                subpaths.append(following)
                continue

            name = module_name
            package_name = parent if parent is not None and parent != "" else os.path.basename(loader.path)

            # following code get name of scenario instead of name of file without actually loading
            # and executing its python code

            source = loader.find_module(module_name).get_source(module_name) # type: str
            prefix = "scenario_name = "
            lines = source.splitlines(False)

            for i, l in enumerate(lines): # type: str
                # source code of scenario template will be always longer than 50 lines
                # but name of scenario should occur in about first 30 lines of code
                # it is magical constant, but it is used only and only on this place
                if i > 50:
                    break

                if l.startswith(prefix):
                    name = l[len(prefix):]
                    name = name.strip().strip('"')
                    break

            self.add_scenario(package_name, name, loader, module_name)

        for path, parent in subpaths:
            self.add_all_scenarios(path, parent)


    class __ScenarioLoaderImpl(object):
        def __init__(self, *arg, **kwords):
            self._scenarios = dict()
            # Logger is not yet available, because this code loads before it can be properly configured
            # print("Scenario loader instance created.")

        def load_scenario(self, group_name: str, scenario_name: str) -> tuple or None:
            if group_name not in self._scenarios.keys():
                return None

            group = self._scenarios[group_name]
            if scenario_name not in group.keys():
                return None

            loader, module_name = group[scenario_name]
            m = loader.find_module(module_name).load_module(module_name)
            return m.scenario

        def add_scenario(self, group_name: str, scenario_name: str, importer: object, module_name: str):
            if group_name not in self._scenarios.keys():
                self._scenarios[group_name] = dict()

            group = self._scenarios[group_name]
            group[scenario_name] = (importer, module_name)

            # Logger is not yet available, because this code loads before it can be properly configured
            # print("Scenario added to loader.")
