#!/usr/bin/env python3
#
# Framewor for testing web aplications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.element import Element

class MockElement(Element):

    def __init__(self, tag: str, id: str="", classname: str="", text: str="mock element", width: int=0, height: int=0):
        self._elem = self
        self._tag_name = tag
        self._id = id
        self._classname = classname
        self._text_node = text
        self._width = width
        self._height = height

    def __eq__(self, elem):
        return self._elem == elem._elem

    def __ne__(self, element):
        return not self.__eq__(element)

    def __str__(self):
        pattern = '<{0} id="{1}" class="{2}" width="{4}" height="{5}">{3}<{0}/>\n'
        return pattern.format(self._tag_name, self._id, self._classname, self._text_node, self._width, self.height)

    # attributes and properties of element -------------------------------------------------
    @property
    def id(self):
        self._elem.id

    @property
    def classname(self):
        return ""

    @property
    def tag_name(self):
        return self._elem.tag_name

    @property
    def text(self):
        return self._elem.text

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def selected(self):
        return False

    @property
    def enabled(self):
        return False

    def get_property(self, name: str):
        return ""

    def get_attribute(self, name: str):
        return ""

    def get_size(self):
        return {"width" : self.width, "height" : self.height}

    def get_css_property_value(self, property_name: str):
        return ""

    # searching for inner elements -------------------------------------------------
    def find_element_by_id(self, id: str):
        if id == self._id:
            return self
        return None

    def find_elements_by_id(self, id: str):
        elem_list = list()
        if id == self._id:
             elem_list.append(self)
        return elem_list

    def find_element_by_class_name(self, classname: str):
        if classname == self._classname:
            return self
        return None

    def find_elements_by_class_name(self, classname: str):
        elem_list = list()
        if classname == self._classname:
            elem_list.append(self)
        return elem_list

    def find_element_by_tag_name(self, tagname: str):
        if tagname == self._tag_name:
            return self
        return None

    def find_elements_by_tag_name(self, tagname: str):
        elem_list = list()
        if tagname == self._tag_name:
            elem_list.append(self)
        return elem_list

    def find_element_by_name(self, name: str):
        return None

    def find_elements_by_name(self, name: str):
        return list()

    def find_element_by_xpath(self, xpath: str):
        return self

    def find_elements_by_xpath(self, xpath: str):
        return list()

    def find_element_by_link_text(self, link_text: str):
        return None

    def find_elements_by_link_text(self, link_text: str):
        return list()

    def find_element_by_partial_link_text(self, link_text: str):
        return None

    def find_elements_by_partial_link_text(self, link_text: str):
        return list()

    def find_element_by_css_selector(self, css_selector: str):
        return None

    def find_elements_by_css_selector(self, css_selector: str):
        return list()

    # actions performed on element -------------------------------------------------

#    def location_once_scrolled_into_view(self):

    def click(self):
        pass

    def submit(self):
        pass

    def clear(self):
        pass

#    def location(self):

#    def screenshot_as_base64(self):

#    def screenshot_as_png(self):

#    def screenshot(self, filename: str):



