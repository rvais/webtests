#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from webtest.common.logger import get_logger
from webtest.common.wait_for import Wait

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

    @Wait
    def get_property(self, name: str):
        return self._elem.get_property(name)

    @Wait
    def get_attribute(self, name: str):
        return  self._elem.get_attribute(name)

    def get_size(self):
        return self._elem.size

    @Wait
    def get_css_property_value(self, property_name: str):
        return self._elem.value_of_css_property(property_name)

    # searching for inner elements -------------------------------------------------

    @Wait
    def find_element_by_id(self, id: str):
        return Element(self._elem.find_element_by_id(id))

    @Wait
    def find_elements_by_id(self, id: str):
        element_list = list()
        for elm in self._elem.find_elements_by_id(id):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element_by_class_name(self, classname: str):
        return Element(self._elem.find_element_by_class_name(classname))

    @Wait
    def find_elements_by_class_name(self, classname: str):
        element_list = list()
        for elm in self._elem.find_elements_by_class_name(classname):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element_by_tag_name(self, tagname: str):
        return Element(self._elem.find_element_by_tag_name(tagname))

    @Wait
    def find_elements_by_tag_name(self, tagname: str):
        element_list = list()
        for elm in self._elem.find_elements_by_tag_name(tagname):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element_by_name(self, name: str):
        return Element(self._elem.find_element_by_name(name))

    @Wait
    def find_elements_by_name(self, name: str):
        element_list = list()
        for elm in self._elem.find_elements_by_name(name):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element_by_xpath(self, xpath: str):
        return Element(self._elem.find_element_by_xpath(xpath))

    @Wait
    def find_elements_by_xpath(self, xpath: str):
        element_list = list()
        for elm in self._elem.find_elements_by_xpath(xpath):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element_by_link_text(self, link_text: str):
        return Element(self._elem.find_element_by_link_text(link_text))

    @Wait
    def find_elements_by_link_text(self, link_text: str):
        element_list = list()
        for elm in self._elem.find_elements_by_link_text(link_text):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element_by_partial_link_text(self, link_text: str):
        return Element(self._elem.find_element_by_partial_link_text(link_text))

    @Wait
    def find_elements_by_partial_link_text(self, link_text: str):
        element_list = list()
        for elm in self._elem.find_elements_by_partial_link_text(link_text):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element_by_css_selector(self, css_selector: str):
        return Element(self._elem.find_element_by_css_selector(css_selector))

    @Wait
    def find_elements_by_css_selector(self, css_selector: str):
        element_list = list()
        for elm in self._elem.find_elements_by_css_selector(css_selector):
            element_list.append(Element(elm))

        return element_list

    @Wait
    def find_element(self, selector: str='', value: str=''):
    #def find_element(self, *args):
        logger = get_logger()
    #    logger.debug(str(self), str(args))
        logger.debug("Element call\n{}\n{}\n{}".format(str(self), str(selector), str(value)))
        return Element(self._elem.find_element(by=selector, value=value))

    @Wait
    def get_childnodes(self):
        return self.find_elements_by_xpath('./*')

    # actions performed on element -------------------------------------------------

#    def location_once_scrolled_into_view(self):

    @Wait
    def click(self):
        self._elem.click()
        return True

    @Wait
    def type_in(self, input_text: str):
        return self._elem.send_keys(input_text)

    @Wait
    def submit(self):
        return self._elem.submit()

    @Wait
    def clear(self):
        return self._elem.clear()

    def fill(self, value: dict=None):
        logger = get_logger()
        logger.debug("Element fill call\n{}\n{}".format(str(self), str(value)))

        if isinstance(value, tuple) and self.tag_name == "input":
            return self.fill_input(self, *value)

        elif isinstance(value, tuple) and self.tag_name == "textarea":
            return self.fill_input(self, *value)

        elif isinstance(value, tuple) and self.tag_name == "select":
            return self.fill_select(self, *value)

        elif isinstance(value, list) and self.tag_name == "form":
            return self.fill_form(value)

        else:
            logger.debug("Couldn't identify element to fill")
            return False

    @Wait
    def fill_input(self, node_type: str, value=None, xpath: str=""):
        logger = get_logger()
        logger.debug("input fill call\n{}\n{}\n{}".format(str(self), str(node_type), str(value)))
        inp = self
        if self.tag_name != "input":
            inp = self.find_element_by_xpath(xpath)

        if inp is None or inp.get_attribute(inp, 'type') != node_type:
            return False

        boolean_types = ['checkbox', 'radio']
        text_types = ['date', 'datetime-local', 'email', 'month', 'number',
                      'password', 'range', 'search', 'tel', 'text', 'time', 'url', 'week']

        if (isinstance(value, bool)
            and node_type in boolean_types):
            if inp.selected != value:
                inp.click(inp)

        elif node_type in text_types:
            inp.type_in(inp, str(value))

        else:
            return False

        return True

    @Wait
    def fill_select(self, *options):
        if self.tag_name != "select":
            return False

        element_select = Select(self._elem)
        for opt in options:
            element_select.select_by_value(opt)

        return True

    @Wait
    def fill_form(self, items: list):
        success = True
        logger = get_logger()
        logger.debug("Element fill form\n{}".format(str(items)))
        for xpath, value in items:
            element = self.find_element_by_xpath(xpath)
            success = success and element.fill(value)
        return success

#    def location(self):

#    def screenshot_as_base64(self):

#    def screenshot_as_png(self):

#    def screenshot(self, filename: str):



