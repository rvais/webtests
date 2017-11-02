#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from copy import copy
from selenium.common.exceptions import StaleElementReferenceException

from webtest.common.selector import Selector
from webtest.components.pagemodel.element import WebElement
from webtest.components.pagemodel.mock_element import MockElement
from webtest.components.pagemodel.mock_element import Element
from webtest.common.logging.logger import get_logger

class Component(object):
    def __init__(self, name: str, selector_type: str, selector_value: str, parent: str=None, construction_exclude=False):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._name = name
        self._stype = selector_type
        self._svalue = selector_value
        self._parent = parent
        self._construct = not construction_exclude
        self._root = MockElement("root")
        self._node = MockElement("node")

        self._subcomponents = list()

        self._logger.debug("Component '{}' created.".format(self._name))

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_available(self) -> bool:
        return not isinstance(self._node, MockElement)

    @property
    def visible(self) -> bool:
        return self._node.visible

    @property
    def selector_type(self) -> str:
        return self._stype

    @property
    def selector_value(self) -> str:
        return self._svalue

    @property
    def parent(self) -> str or None:
        return self._parent

    @property
    def construct(self) -> bool:
        return self._parent

    @property
    def tuple(self) -> tuple:
        if self._parent is None:
            return (self._name, self._stype, self._svalue)
        else:
            return (self._name, self._stype, self._svalue, self._parent)


    def set_root(self, root: Element or WebElement) -> bool:
        original_root = self._root # type: MockElement
        original_node = self._node

        try:
            self._logger.debug("Attempting to set new root node <{}> for '{}' component.".format(root.tag_name, self.name))
            self._root = root
            self._node = self._root.get_element(self._root, self._stype, self._svalue)

        except BaseException as ex:
            self._logger.error("Setting new root node for component '{}' was not successful"
                               " and may cause trouble in following code.".format(self.name))
            self._logger.error(ex.args)
            self._root = original_root
            self._node = original_node
            return False

        return True
    
    def get_root_node(self) -> Element or MockElement:
        return self._root

    def get_element_node(self) -> Element or MockElement:
        return self._node

    def get_subcomponents(self) -> list:
        for component in self._subcomponents:
            if not isinstance(self.get_element_node(), MockElement) and component.get_root_node() != self.get_element_node():
                self._logger.debug("Setting root node for subcomponent '{}'.".format(component.name))
                if not component.set_root(self.get_element_node()):
                    raise BaseException("Could not set root node for given component.")

        return copy(self._subcomponents)

    def get_subcomponent(self, name: str="", recursive: bool=False, depth: int=1) -> 'Component':
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

        if found is not None:
            if not isinstance(self.get_element_node(), MockElement) and found.get_root_node() != self.get_element_node():
                self._logger.debug("Setting root node for subcomponent '{}'.".format(found.name))
                if not found.set_root(self.get_element_node()):
                    raise BaseException("Could not set root node for given component.")

        return found

    def add_subcomponent(self, component: 'Component') -> None:
        self._subcomponents.append(component)

    def add_subcomponents(self, components: list) -> None:
        self._subcomponents.extend(components)


    def fill(self, value: dict) -> bool:
        try:
            return self.__fill(value)

        except StaleElementReferenceException as ex:
            self._logger.debug("Inner node is no longer in document. Trying to re-set inner node.")
            self._logger.trace(ex)
            self.set_root(self._root)
            return self.__fill(value)

    def __fill(self, value: dict) -> bool:
        self._logger.debug("Attempt to fill component {} with data {}.".format(self.name, value))

        if isinstance(value, dict):
            success = True
            for subcomponent, item in value.items():
                self._logger.debug("component {}, data {}.".format(subcomponent, item))
                c = self.get_subcomponent(subcomponent)
                tmp = c.fill(item)
                success = success and tmp
            return success

        else:
            return self._node.fill(value)


    def fill_form(self, items: list) -> bool:
        try:
            return self.__fill_form(items)

        except StaleElementReferenceException as ex:
            self._logger.debug("Inner node is no longer in document. Trying to re-set inner node.")
            self._logger.trace(ex)
            self.set_root(self._root)
            return self.__fill_form(items)

    def __fill_form(self, items: list) -> bool:
        return self._node.fill_form(self._node, items)


    def fill_input(self, node_type: str, value, xpath: str="") -> bool:
        try:
            return self.__fill_input(node_type, value, xpath)

        except StaleElementReferenceException as ex:
            self._logger.debug("Inner node is no longer in document. Trying to re-set inner node.")
            self._logger.trace(ex)
            self.set_root(self._root)
            return self.__fill_input(node_type, value, xpath)

    def __fill_input(self, node_type: str, value, xpath: str="") -> bool:
        return self._node.fill_input(self._node, node_type,value, xpath)


    def fill_select(self, *options) -> bool:
        try:
            return self.__fill_select(self, *options)

        except StaleElementReferenceException as ex:
            self._logger.debug("Inner node is no longer in document. Trying to re-set inner node.")
            self._logger.trace(ex)
            self.set_root(self._root)
            return self.__fill_select(self, *options)

    def __fill_select(self, *options) -> bool:
        return self._node.fill_select(self._node,options)


    def click(self) -> bool:
        try:
            return self.__click()

        except StaleElementReferenceException as ex:
            self._logger.debug("Inner node is no longer in document. Trying to re-set inner node.")
            self._logger.trace(ex)
            self.set_root(self._root)
            return self.__click()

    def __click(self) -> bool:
        return self._node.click(self._node)


class RootComponent(Component):
    def __init__(self, root: Element):
        super(RootComponent, self).__init__(self, "root", Selector.XPATH, '//')

        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._root = root
        self._node = root

        self._logger.debug("Root component '{}' created.".format(self._name))
