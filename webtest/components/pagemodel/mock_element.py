#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.element import Element

class MockElement(Element):

    def __init__(self, tag: str, id: str = "", classname: str = "", text: str = "mock element", width: int = 0, height: int = 0):
        super(MockElement, self).__init__(None)

        self._elem = self
        self._tag_name = tag
        self._id = id
        self._classname = classname
        self._text_node = text
        self._width = width
        self._height = height

    def __eq__(self, elem):
        return isinstance(elem, MockElement) and str(self._elem) == str(elem)

    def __ne__(self, element):
        return not self.__eq__(element)

    def __str__(self):
        pattern = '<{0} id="{1}" class="{2}" width="{4}" height="{5}">{3}<{0}/>\n'
        return pattern.format(self._tag_name, self._id, self._classname, self._text_node, self._width, self.height)

    # property and attribute getters __________________________________________
    # stable properties
    def _get_stable_properties(self):
        pass

    def get_id(self, refresh: bool=False) -> str:
        return self._id

    def get_class_name(self, refresh: bool = False) -> str:
        return self._classname

    def get_tag_name(self, refresh: bool = False) -> str:
        return self._tag_name

    def get_size(self, refresh: bool = False) -> dict:
        return self._size

    def get_text(self, refresh: bool = False) -> str:
        return self._text_node

    def get_width(self, refresh: bool = False) -> int:
        return self.get_size(refresh)["width"]

    def get_height(self, refresh: bool = False) -> int:
        return self.get_size(refresh)["height"]

    # unstable properties that require to be queried every time
    @property
    def visible(self) -> bool:
        return False

    @property
    def selected(self) -> bool:
        return False

    @property
    def enabled(self) -> bool:
        return False

    def get_css_property(self, name: str) -> str:
        return ""

    def get_attribute(self, name: str) -> str:
        return  ""

    def get_css_property_value(self, property_name: str) -> str:
        return ""

    # searching for elements
    def get_element(self, selector: str, value: str) -> 'Element' or None:
        log_message = "Searching for element by '{selector}', with '{value}' in MockElement!"
        self._logger.warning(log_message.format(selector=selector, value=value))
        return None

    def get_multiple_elements(self, selector: str, value: str) -> list:
        log_message = "Searching for multiple elements by '{selector}', with '{value}' in MockElement!"
        self._logger.warning(log_message.format(selector=selector, value=value))
        return list()

    # actions performed on element
    def click(self):
        self._logger.warning("Attempt to click on MockElement!")
        return False

    def type_in(self, input_text: str):
        self._logger.warning("Attempt to fill text {} in MockElement!".format(input_text))
        return False

    def submit(self):
        self._logger.warning("Attempt to perform submit MockElement!")
        return False

    def clear(self):
        self._logger.warning("Attempt to perform clear MockElement!")
        return False

