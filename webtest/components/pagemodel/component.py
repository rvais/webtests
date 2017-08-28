#!/usr/bin/env python3
#
# Framewor for testing web aplications - proof of concept
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
            self._logger.debug("Attempting to set new root node for this component.")
            self._root = root
            self._node = self._root.find_element(self.tuple)

            for subcomp in self._subcomponents:
                if not subcomp.set_root(self._node):
                    raise Exception()

        except Exception as ex:
            self._logger.error("Setting new root node for this component was not successful"
                               " and may cause trouble in following code.")
            self._root = original_root
            self._node = original_node
            return False

        return True
    
    def get_element_node(self):
        return self._node

    def get_subcomponents(self):
        return copy(self._subcomponents)

    def add_subcomponent(self, component: 'Component'):
        self._subcomponents.append(component)

    def add_subcomponents(self, components: list):
        self._subcomponents.extend(components)






