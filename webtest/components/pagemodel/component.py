#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from copy import copy
from webtest.components.pagemodel.element import WebElement
from webtest.components.pagemodel.mock_element import MockElement
from webtest.common.logger import get_logger

class Component(object):
    def __init__(self, name: str, selector_type: str, selector_value: str, parent: str=None):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._name = name
        self._stype = selector_type
        self._svalue = selector_value
        self._parent = parent
        self._root = MockElement("root")
        self._node = MockElement("node")

        self._subcomponents = list()

    @property
    def name(self):
        return self._name

    @property
    def selector_type(self):
        return self._stype

    @property
    def selector_value(self):
        return self._svalue

    @property
    def parent(self):
        return self._parent

    @property
    def tuple(self):
        if self._parent is None:
            return (self._name, self._stype, self._svalue)
        else:
            return (self._name, self._stype, self._svalue, self._parent)


    def set_root(self, root: WebElement):
        original_root = self._root
        original_node = self._node

        try:
            self._logger.debug("Attempting to set new root node <{}> for this component.".format(root.tag_name))
            self._root = root
            self._node = self._root.find_element(self._stype, self._svalue)

            # if self._subcomponents

            for comp in self._subcomponents:
                self._logger.debug("Setting root node for subcomponent '{}'.".format(str(comp)))
                if not comp.set_root(self._node):
                    raise Exception()

        except Exception as ex:
            self._logger.error("Setting new root node for this component was not successful"
                               " and may cause trouble in following code.")
            self._logger.error(ex.args)
            self._root = original_root
            self._node = original_node
            return False

        return True
    
    def get_element_node(self):
        return self._node

    def get_subcomponents(self):
        return copy(self._subcomponents)

    def get_subcomponent(self, name: str="", recursive: bool=False, depth: int=1):
        if name is None or not len(name) > 0:
            return None

        found = None
        for comp in self._subcomponents:
            if comp.name == name:
                found = comp
                break
            if recursive and depth > 0:
                found = comp.get_subcomponent(name, recursive, depth - 1)
                if found is not None:
                    break

        return found

    def add_subcomponent(self, component: 'Component'):
        self._subcomponents.append(component)

    def add_subcomponents(self, components: list):
        self._subcomponents.extend(components)

    def fill(self, value: dict):
        self._logger.debug("Attempt to fill component {} with data.".format(self.name))

        if isinstance(value, dict):
            success = True
            for subcomponent, item in value.items():
                success = success and self[subcomponent].fill(item)

            return success

        else:
            return self._node.fill(value)

    def fill_input(self, node_type: str, value, xpath: str=""):
        return self._node.fill_input(node_type,value, xpath)

    def fill_select(self, *options):
        return self._node.fill_select(options)

    def fill_form(self, items: list):
        return self._node.fill_form(items)

    def click(self):
        return self._node.click()

