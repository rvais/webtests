#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

class Element(object):

    def __init__(self, webelem: WebElement):
        self._elem = webelem

    def __eq__(self, elem):
        return self._elem == elem._elem

    def __ne__(self, element):
        return not self.__eq__(element)

    # attributes and properties of element -------------------------------------------------
    @property
    def id(self):
        return self._elem.id

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
        return self._elem.size["width"]

    @property
    def height(self):
        return self._elem.size["height"]

    @property
    def selected(self):
        return self._elem.is_selected()

    @property
    def enabled(self):
        return self._elem.is_enabled()

    def get_property(self, name: str):
        return self._elem.get_property(name)

    def get_attribute(self, name: str):
        return  self._elem.get_attribute(name)

    def get_size(self):
        return self._elem.size

    def get_css_property_value(self, property_name: str):
        return self._elem.value_of_css_property(property_name)

    # searching for inner elements -------------------------------------------------
    def find_element_by_id(self, id: str):
        return Element(self._elem.find_element_by_id(id))

    def find_elements_by_id(self, id: str):
        element_list = list()
        for elm in self._elem.find_elements_by_id(id):
            element_list.append(Element(elm))

        return element_list

    def find_element_by_class_name(self, classname: str):
        return Element(self._elem.find_element_by_class_name(classname))

    def find_elements_by_class_name(self, classname: str):
        element_list = list()
        for elm in self._elem.find_elements_by_class_name(classname):
            element_list.append(Element(elm))

        return element_list

    def find_element_by_tag_name(self, tagname: str):
        return Element(self._elem.find_element_by_tag_name(tagname))

    def find_elements_by_tag_name(self, tagname: str):
        element_list = list()
        for elm in self._elem.find_elements_by_tag_name(tagname):
            element_list.append(Element(elm))

        return element_list

    def find_element_by_name(self, name: str):
        return Element(self._elem.find_element_by_name(name))

    def find_elements_by_name(self, name: str):
        element_list = list()
        for elm in self._elem.find_elements_by_name(name):
            element_list.append(Element(elm))

        return element_list

    def find_element_by_xpath(self, xpath: str):
        return Element(self._elem.find_element_by_xpath(xpath))

    def find_elements_by_xpath(self, xpath: str):
        element_list = list()
        for elm in self._elem.find_elements_by_xpath(xpath):
            element_list.append(Element(elm))

        return element_list

    def find_element_by_link_text(self, link_text: str):
        return Element(self._elem.find_element_by_link_text(link_text))

    def find_elements_by_link_text(self, link_text: str):
        element_list = list()
        for elm in self._elem.find_elements_by_link_text(link_text):
            element_list.append(Element(elm))

        return element_list

    def find_element_by_partial_link_text(self, link_text: str):
        return Element(self._elem.find_element_by_partial_link_text(link_text))

    def find_elements_by_partial_link_text(self, link_text: str):
        element_list = list()
        for elm in self._elem.find_elements_by_partial_link_text(link_text):
            element_list.append(Element(elm))

        return element_list

    def find_element_by_css_selector(self, css_selector: str):
        return Element(self._elem.find_element_by_css_selector(css_selector))

    def find_elements_by_css_selector(self, css_selector: str):
        element_list = list()
        for elm in self._elem.find_elements_by_css_selector(css_selector):
            element_list.append(Element(elm))

        return element_list

    def find_element(self, selector: str, value: str):
        return Element(self._elem.find_element(by=selector, value=value))

    def get_childnodes(self):
        return self.find_elements_by_xpath('./*')

    # actions performed on element -------------------------------------------------

#    def location_once_scrolled_into_view(self):

    def click(self):
        self._elem.click()
        return True

    def type_in(self, input_text: str):
        return self._elem.send_keys(input_text)

    def submit(self):
        return self._elem.submit()

    def clear(self):
        return self._elem.clear()

    def fill(self, value: dict):

        if isinstance(value, tuple) and self.tag_name == "input":
            return self.fill_input(*value)

        elif isinstance(value, tuple) and self.tag_name == "textarea":
            return self.fill_input(*value)

        elif isinstance(value, tuple) and self.tag_name == "select":
            return self.fill_select(*value)

        elif isinstance(value, list) and self.tag_name == "form":
            return self.fill_form(value)

        else:
            return False

    def fill_input(self, node_type: str, value, xpath: str=""):
        if self.tag_name != "input":
            return self.find_element_by_xpath(xpath)

        if self.get_attribute('type') != node_type:
            return False

        boolean_types = ['checkbox', 'radio']
        text_types = ['date', 'datetime-local', 'email', 'month', 'number',
                      'password', 'range', 'search', 'tel', 'text', 'time', 'url', 'week']

        if (isinstance(value, bool)
            and node_type in boolean_types):
            if self.selected != value:
                self.click()

        elif node_type in text_types:
            self.type_in(str(value))

        else:
            return False

        return True

    def fill_select(self, *options):
        if self.tag_name != "select":
            return False

        element_select = Select(self._elem)
        for opt in options:
            element_select.select_by_value(opt)

        return True

    def fill_form(self, items: list):
        success = True
        for xpath, value in items:
            element = self.find_element_by_xpath(xpath)
            success = success and element.fill(value)
        return success

#    def location(self):

#    def screenshot_as_base64(self):

#    def screenshot_as_png(self):

#    def screenshot(self, filename: str):



