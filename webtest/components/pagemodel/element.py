#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from webtest.common.logging.logger import get_logger
from webtest.common.selector import Selector
from webtest.common.wait_for import Wait

class Element(object):

    _input_boolean_types = ['checkbox', 'radio']
    _input_text_types = ['date', 'datetime-local', 'email', 'month', 'number',
                  'password', 'range', 'search', 'tel', 'text', 'time', 'url', 'week']

    def __init__(self, webelem: WebElement or None):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        # setup default values
        self._elem = webelem    # type: WebElement
        self._id = "#id"
        self._classname = ""
        self._tag_name = "elem"
        self._size = {
            "width" : 0,
            "height" : 0,
        }
        self._text_node = ""

        # query the stable properties of the element (if possible only once)
        self._get_stable_properties()

        # prepare dictionary that will serve as switch-case for fill_* methods
        self._fill_element = {
            "form": self.fill_form,
            "input" : self.fill_input,
            "select" : self.fill_select,
            "textarea" : self.fill_textarea,
        }

    def __eq__(self, elem):
        return self._elem == elem._elem

    def __ne__(self, element):
        return not self.__eq__(element)

    def __str__(self):
        try:
            return "'<{}> element'".format(self._tag_name)
        except BaseException as ex:
            return super(Element, self).__str__()

    # property and attribute getters __________________________________________
    # stable properties
    def _get_stable_properties(self):
        self._id = self.get_id(self, True)
        self._classname = self.get_class_name(self, True)
        self._tag_name = self.get_tag_name(self, True)
        self._size = self.get_size(self, True)
        self._text_node = self.get_text(self, True)
        self._input_type = None
        if isinstance(self._tag_name, str) and self._tag_name.lower()  == "input":
            self._input_type = self.get_attribute(self, "type")

        return

    @property
    def id(self) -> str:
        return self.get_id()

    @Wait
    def get_id(self, refresh: bool=False) -> str:
        if refresh:
            self._logger.trace("Refreshing value of 'id' property")
            self._id = self._elem.id

        return self._id

    @property
    def class_name(self) -> str:
        return self.get_class_name()

    @Wait
    def get_class_name(self, refresh: bool = False) -> str:
        if refresh:
            self._logger.trace("Refreshing value of 'class' property")
            self._classname = self.get_attribute(self, "class")

        return self._classname

    @property
    def tag_name(self) -> str:
        return self.get_tag_name(self)

    @Wait
    def get_tag_name(self, refresh: bool = False) -> str:
        if refresh:
            self._logger.trace("Refreshing value of 'tag name' property")
            self._tag_name = self._elem.tag_name

        return self._tag_name

    @property
    def size(self) -> dict:
        return self.get_size()

    @Wait
    def get_size(self, refresh: bool = False) -> dict:
        if refresh:
            self._logger.trace("Refreshing value of 'size' property")
            self._size = self._elem.size

        return self._size

    @property
    def text(self) -> str:
        return self.get_text()

    @Wait
    def get_text(self, refresh: bool = False) -> str:
        if refresh:
            self._logger.trace("Refreshing value of element's inner text")
            self._text_node = self._elem.text

        return self._text_node

    def get_width(self, refresh: bool = False) -> int:
        return self.get_size(refresh)["width"]

    def get_height(self, refresh: bool = False) -> int:
        return self.get_size(refresh)["height"]

    # unstable properties that require to be queried every time
    @property
    @Wait
    def visible(self) -> bool:
        return self._elem.is_displayed()

    @property
    @Wait
    def selected(self) -> bool:
        return self._elem.is_selected()

    @property
    @Wait
    def enabled(self) -> bool:
        return self._elem.is_enabled()

    @Wait
    def get_css_property(self, name: str) -> str:
        return self._elem.get_property(name)

    @Wait
    def get_attribute(self, name: str) -> str:
        return  self._elem.get_attribute(name)

    @Wait
    def get_css_property_value(self, property_name: str) -> str:
        return self._elem.value_of_css_property(property_name)

    def get_inner_node(self):
        return self._elem;

    # find specific single element node passing given criteria ________________
    @Wait
    def get_element(self, selector: str, value: str) -> 'Element' or None:
        log_message = "Searching for element by '{selector}', with '{value}'."
        self._logger.debug(log_message.format(selector=selector, value=value))
        raw_node = self._elem.find_element(selector, value)
        if not  isinstance(raw_node, WebElement):
            return None

        return Element(raw_node)

    def get_element_by_id(self, id) -> 'Element' or None:
        return self.get_element(self, selector=Selector.ID, value=id)

    def get_element_by_tag_name(self, name) -> 'Element' or None:
        return self.get_element(self, selector=Selector.TAG_NAME, value=name)

    def get_element_by_class_name(self, class_name) -> 'Element' or None:
        return self.get_element(self, selector=Selector.CLASS_NAME, value=class_name)

    def get_element_by_name_property(self, name) -> 'Element' or None:
        return self.get_element(self, selector=Selector.NAME_PROPERTY, value=name)

    def get_link_by_text(self, link_text) -> 'Element' or None:
        return self.get_element(self, selector=Selector.LINK_TEXT, value=link_text)

    def get_link_by_partial_text(self, link_text) -> 'Element' or None:
        return self.get_element(self, selector=Selector.PARTIAL_LINK_TEXT, value=link_text)

    def get_element_by_xpath(self, xpath) -> 'Element' or None:
        return self.get_element(self, selector=Selector.XPATH, value=xpath)

    def get_element_by_css_selector(self, css_selector) -> 'Element' or None:
        return self.get_element(self, selector=Selector.CSS, value=css_selector)

    def _get_neighbour(
            self,
            tag_name: str='node()',
            excludes: iter or None='self::text()',
            filters: iter or None=None,
            selector: str='following-sibling',
            index='1'
        ) -> 'Element' or None:

        excluded = list()

        if isinstance(excludes, list) or isinstance(excludes, tuple):
            for exclude in excludes:
                excluded.append("[not({})]".format(exclude))

        elif excludes and isinstance(excludes, str):
            excluded.append("[not({})]".format(excludes))

        exclude = "".join(excluded)

        attributes = list()
        if isinstance(filters, list) or isinstance(filters, tuple):
            for attr in filters:
                attributes.append("[{}]".format(attr))

        elif filters and isinstance(filters, str):
            attributes.append("[{}]".format(filters))

        attr = "".join(attributes)

        xpath_format = '//{selector}::{tag_name}{exclude}{attributes}[index]'
        xpath = xpath_format.format(
            selector=selector,
            tag_name=tag_name,
            exclude=exclude,
            attributes=attr,
            index=index
        )
        return self.get_element(selector=Selector.XPATH, value=xpath)

    def get_parent(self) -> 'Element' or None:
        return self.get_element(selector=Selector.XPATH, value='//parent::node()')

    def get_prev_sibling(
            self,
            tag_name: str='node()',
            excludes: iter='self::text()',
            filters: iter or None=None
        ) -> 'Element' or None:
        return self._get_neighbour(tag_name, excludes, filters, 'preceding-sibling')

    def get_next_sibling(
            self,
            tag_name: str='node()',
            excludes: iter='self::text()',
            filters: iter or None=None
        ) -> 'Element' or None:
        return self._get_neighbour(tag_name, excludes, filters, 'following-sibling')

    def get_first_child(
            self,
            tag_name: str='node()',
            excludes: iter='self::text()',
            filters: iter or None = None,
    ) -> 'Element' or None:
        return self._get_neighbour(tag_name, excludes, filters, 'child')

    def get_last_child(
            self,
            tag_name: str='node()',
            excludes: iter='self::text()',
            filters: iter or None = None,
        ) -> 'Element' or None:
        return self._get_neighbour(tag_name, excludes, filters, 'child', index='last()')

    # find multiple element nodes passing given criteria ______________________
    @Wait
    def get_multiple_elements(self, selector: str, value: str) -> list:
        log_message = "Searching for multiple elements by '{selector}', with '{value}'."
        self._logger.trace(log_message.format(selector=selector, value=value))

        element_list = list()
        result = self._elem.find_elements(by=selector, value=value)
        if isinstance(result, list):
            for item in result:
                if isinstance(item, WebElement):
                    element_list.append(Element(item))

        elif isinstance(result, WebElement):
            element_list.append(Element(result))

        return element_list

    def get_elements_by_tag_name(self, name) -> list:
        return self.get_multiple_elements(self, selector=Selector.TAG_NAME, value=name)

    def get_elements_by_class_name(self, class_name) -> list:
        return self.get_multiple_elements(self, selector=Selector.CLASS_NAME, value=class_name)

    def get_elements_by_name_property(self, name) -> list:
        return self.get_multiple_elements(self, selector=Selector.NAME_PROPERTY, value=name)

    def get_links_by_text(self, link_text) -> list:
        return self.get_multiple_elements(self, selector=Selector.LINK_TEXT, value=link_text)

    def get_links_by_partial_text(self, link_text) -> list:
        return self.get_multiple_elements(self, selector=Selector.PARTIAL_LINK_TEXT, value=link_text)

    def get_elements_by_xpath(self, xpath) -> list:
        return self.get_multiple_elements(self, selector=Selector.XPATH, value=xpath)

    def get_elements_by_css_selector(self, css_selector) -> list:
        return self.get_multiple_elements(self, selector=Selector.CSS, value=css_selector)

    def _get_multiple_neighbours(
            self,
            tag_name: str='node()',
            excludes: iter='self::text()',
            filters: iter or None = None,
            selector: str='following-sibling') -> list:

        excluded = list()

        if isinstance(excludes, list) or isinstance(excludes, tuple):
            for exclude in excludes:
                excluded.append("[not({})]".format(exclude))

        elif excludes and isinstance(excludes, str):
            excluded.append("[not({})]".format(excludes))

        exclude = "".join(excluded)

        attributes = list()
        if isinstance(filters, list) or isinstance(filters, tuple):
            for attr in filters:
                attributes.append("[{}]".format(attr))

        elif filters and isinstance(filters, str):
            attributes.append("[{}]".format(filters))

        attr = "".join(attributes)

        xpath_format = '//{selector}::{tag_name}{exclude}{attributes}'
        xpath = xpath_format.format(
            selector=selector,
            tag_name=tag_name,
            exclude=exclude,
            attributes=attr
        )
        return self.get_multiple_elements(selector=Selector.XPATH, value=xpath)

    def get_all_siblings(
            self,
            tag_name: str = 'node()',
            excludes: iter = 'self::text()',
            filters: iter or None = None
        ) -> list:
        siblings = list()
        siblings.extend(self._get_multiple_neighbours(tag_name, excludes, filters, 'preceding-sibling'))
        siblings.extend(self._get_multiple_neighbours(tag_name, excludes, filters, 'following-sibling'))
        return siblings

    def get_child_nodes(
            self,
            tag_name: str = 'node()',
            excludes: iter = 'self::text()',
            filters: iter or None = None
        ) -> list:
        return self._get_multiple_neighbours(tag_name, excludes, filters, 'child')

    def get_all_descendants(
            self,
            tag_name: str = 'node()',
            excludes: iter = 'self::text()',
            filters: iter or None = None
        ) -> list:
        return self._get_multiple_neighbours(tag_name, excludes, filters, '*')

    # perform action on element (self) ________________________________________
    # TODO: implement following methods if/when useful
    #    def location(self):
    #    def screenshot_as_base64(self):
    #    def screenshot_as_png(self):
    #    def screenshot(self, filename: str):

    @Wait
    def click(self) -> bool:
        self._logger.trace("Performing click on element '{}'.".format(self))
        if self.visible:
            self._elem.click()
            return True

        self._logger.trace("Element '{}' is not visible.".format(self))
        return False

    @Wait
    def type_in(self, input_text: str) -> bool:
        self._logger.trace("Trying to type text '{}' in element '{}'.".format(input_text, self))
        if self.visible:
            return self._elem.send_keys(input_text)

        self._logger.trace("Element '{}' is not visible.".format(self))
        return False

    @Wait
    def submit(self) -> bool:
        self._logger.trace("Trying to perform 'submit' on element '{}'.".format(self))
        if self.visible:
            return self._elem.submit()

        self._logger.trace("Element '{}' is not visible.".format(self))
        return False

    @Wait
    def clear(self) -> bool:
        self._logger.trace("Trying to perform clear on element '{}'.".format(self.__str__()))
        if self.visible:
            try:
                return self._elem.clear()
            except InvalidElementStateException as ex:
                self._logger.exception("Couldn't perform 'clear' action on '{}' element {}.\n\texception: "
                                       .format(self._tag_name, self, ex.__str__()))

        self._logger.trace("Element '{}' is not visible.".format(self))
        return False

    @Wait
    def scroll_into_view(self) -> bool:
        self._logger.trace("Trying to check visibility and scroll element '{}' into view.".format(self))
        # TODO: implement this method
        # location_once_scrolled_into_view():
        return False

    # perform action on element that is supposed to be component of form (self)
    def fill(self, value: tuple or list or str) -> bool:
        self._logger.trace("Trying to perform 'fill' action on <{}> element.".format(self.tag_name))
        if self.tag_name not in self._fill_element.keys():
            self._logger.debug("Element <{}> is not one of the predefined "
                               "elements that support 'fill' action.".format(self.tag_name))
            return False

        if not self.visible:
            self._logger.trace("Element '{}' is not visible.".format(self))
            return False

        success = self._fill_element[self.tag_name](self, value)
        self._logger.trace("'fill' action on <{}> element success = '{}' .".format(self.tag_name, success))
        return success


    def fill_form(self, items: list) -> bool:
        if self.tag_name != 'form':
            self._logger.warning("Attempt to act as if <{}> was <form> element".format(self.tag_name))

        if not self.visible:
            self._logger.trace("Element '{}' is not visible.".format(self))
            return False

        # expected result of operation
        success = True

        input_type_list = list()
        input_type_list.extend(Element._input_boolean_types)
        input_type_list.extend(Element._input_text_types)

        self._logger.debug("Element fill form\n{}".format(str(items)))
        for data in items:
            # check if we are looking for
            if len(data) == 3:
                node_type, value, name = data
            else:
                node_type, value = data
                name = None

            attr_filter = list()
            if node_type in input_type_list:
                attr_filter.append('@type="{}"'.format(type))
                node_type = 'input'

            if name is not None:
                attr_filter.append('@name="{}"'.format(name))

            # try to get some input or text area or what ever inside of form
            input_node = self._get_neighbour(node_type, filters=attr_filter, selector='*')
            # if anything fails, it is as if everything would fail
            if input_node is None:
                # we already failed, fart of form won't be filled
                success = False
            else:
                # add the result to what happened so far
                success = success and input_node.fill(data)
        return success

    @Wait
    def fill_input(self, data: tuple or list) -> bool:
        if self.tag_name != 'input':
            self._logger.warning("Attempt to act as if <{}> was <input> element".format(self.tag_name))
            return False

        if not self.visible:
            self._logger.trace("Element '{}' is not visible.".format(self))
            return False

        if len(data) == 2:
            data = list(data)
            data.append(None)

        input_type, value, name = tuple(data)
        if name is not None:
            trace_message = "Input name has been defined as '{}'."
            self._logger.trace(trace_message.format(self, input_type, value, name))
            node_name = self.get_attribute('name')
            if node_name != name:
                warning = "Name '{}' of current <input> element is not equal to declared name '{}'!"
                self._logger.warning(warning.format(node_name, name))
                return False

        trace_message = "Input fill call\n\tself: {}\n\tnode_type: {}\n\tvalue: {}\n\tname: {}"
        self._logger.trace(trace_message.format(self, input_type, value, name))

        if  self.get_attribute(self, 'type') != input_type:
            self._logger.warning("input.get_attribute('type') != {}".format(input_type))
            return False

        if isinstance(value, bool) and input_type in Element._input_boolean_types:
            if self.selected != value:
                return self.click(self)

        elif input_type in Element._input_text_types:
            self.clear(self)
            self.type_in(self, str(value))

        else:
            self._logger.warning("Value is not boolean and node is not on the list "
                                 "of nodes accepting text/number values.")
            return False

        return True

    @Wait
    def fill_select(self, options: list) -> bool:
        if self.tag_name != 'select':
            self._logger.warning("Attempt to act as if <{}> was <select> element".format(self.tag_name))
            return False

        if not self.visible:
            self._logger.trace("Element '{}' is not visible.".format(self))
            return False

        self.clear(self)
        element_select = Select(self._elem)
        for opt in options:
            element_select.select_by_visible_text(opt)

        return True

    @Wait
    def fill_textarea(self, data: str or list or tuple) -> bool:
        if self.tag_name != 'textarea':
            self._logger.warning("Attempt to act as if <{}> was <textarea> element".format(self.tag_name))

        if not self.visible:
            self._logger.trace("Element '{}' is not visible.".format(self))
            return False

        self.clear(self)
        if not isinstance(data,str):
            text = "\n".join(list(data))
        else:
            text = data
        return self.type_in(text)