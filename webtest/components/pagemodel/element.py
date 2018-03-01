#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from webtest.common.logging.logger import get_logger
from webtest.common.selector import Selector
from webtest.common.wait_for import Wait


class Element(object):
    """Class that is supposed to represent DOM element (node)

    Class is complete remapping of Selenium WebElement interface with some modifications like renaming of some
    methods or slight changes in method signatures. There fore the interface was copy-pasted and not inherited.
    Some functionality is added, some removed. This class serves as proxy/wrapper to Selenium's WebElement
    to provide more intuitive and comfortable interface - at least for me. ;-)

    Methods for getting other DOM elements (nodes) - i.e. get_element_by_*() ; get_*_sibling ;
    get_*_child() - are designed (including name convention) to reflect their javascript equivalent.
    Some of them are "helper" methods that are not implemented by Selenium it self.
    """

    _input_boolean_types = ['checkbox', 'radio']
    _input_text_types = ['date', 'datetime-local', 'email', 'month', 'number',
                         'password', 'range', 'search', 'tel', 'text', 'time', 'url', 'week']

    def __init__(self, webelem: WebElement or None):
        """Constructor for Element

        None can be used only by MockElement. Otherwise most of the calls wil fail because None object
        doesn't implement delegated functionality.

        :param webelem: Original Selenium web driver WebElement object that will be encapsulated
        :type webelem: WebElement | None
        """
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        # setup default values
        self._elem = webelem  # type: WebElement
        self._id = "#id"
        self._classname = ""
        self._tag_name = "elem"
        self._size = {
            "width": 0,
            "height": 0,
        }
        self._text_node = ""

        # query the stable properties of the element (if possible only once)
        self._get_stable_properties()

        # prepare dictionary that will serve as switch-case for fill_* methods
        self._fill_element = {
            "form": self.fill_form,
            "input": self.fill_input,
            "select": self.fill_select,
            "textarea": self.fill_textarea,
        }

    def __eq__(self, elem):
        # Elements are equal, if their delegates (WebElements) are.
        return self._elem == elem._elem

    def __ne__(self, element):
        return not self.__eq__(element)

    def __str__(self):
        try:
            return "'<{}> element'".format(self._tag_name)
        except WebDriverException as ex:
            self._logger.warn("WebDriverException has occurred while getting element tag_name.")
            return super(Element, self).__str__()

    # property and attribute getters __________________________________________
    # stable properties
    def _get_stable_properties(self) -> None:
        """Method serves as init for Element"""
        self._id = self.get_id(self, True)
        self._classname = self.get_class_name(self, True)
        self._tag_name = self.get_tag_name(self, True)
        self._size = self.get_size(self, True)
        self._text_node = self.get_text(self, True)
        self._input_type = None
        if isinstance(self._tag_name, str) and self._tag_name.lower() == "input":
            self._input_type = self.get_attribute(self, "type")

    @property
    def id(self) -> str:
        """Element id attribute.

        :return: Element id attribute.
        :rtype: str
        """
        return self.get_id()

    @property
    def internal_id(self) -> str:
        """Unique id used internally by python selenium attribute.

        :return: Unique id used internally by python selenium attribute.
        :rtype: str
        """
        return self._elem.id

    @Wait
    def get_id(self, refresh: bool = False) -> str:
        """Retrieves element id attribute.

        :param refresh: If True, method will access web driver, otherwise returns cached value.
        :type refresh: bool
        :return: Element id attribute.
        :rtype: str
        """
        if refresh:
            self._logger.trace("Refreshing value of 'id' property")
            self._id = self.get_attribute(self, "id")

        return self._id

    @property
    def class_name(self) -> str:
        """Element class attribute (possibly multiple classes in one string as in HTML).

        :return: Element class attribute (possibly multiple classes in one string as in HTML).
        :rtype: str
        """
        return self.get_class_name()

    @Wait
    def get_class_name(self, refresh: bool = False) -> str:
        """Retrieves element class attribute (possibly multiple classes in one string as in HTML).

        :param refresh: If True, method will access web driver, otherwise returns cached value.
        :type refresh: bool
        :return: Element class attribute (possibly multiple classes in one string as in HTML).
        :rtype: str
        """
        if refresh:
            self._logger.trace("Refreshing value of 'class' property")
            self._classname = self.get_attribute(self, "class")

        return self._classname

    @property
    def tag_name(self) -> str:
        """Element tag name as in HTML.

        :return: Element tag name as in HTML.
        :rtype: str
        """
        return self.get_tag_name(self)

    @Wait
    def get_tag_name(self, refresh: bool = False) -> str:
        """Retrieves element tag name as in HTML.

        :param refresh: If True, method will access web driver, otherwise returns cached value.
        :type refresh: bool
        :return: Element tag name as in HTML.
        :rtype: str
        """
        if refresh:
            self._logger.trace("Refreshing value of 'tag name' property")
            self._tag_name = self._elem.tag_name

        return self._tag_name

    @property
    def size(self) -> dict:
        """Dictionary with dimensions of this element

        Dictionary has format like in following example: {"height": 0, "width": 0}

        :return: Dictionary with dimensions of this element
        :rtype: dict[int]
        """
        return self.get_size()

    @Wait
    def get_size(self, refresh: bool = False) -> dict:
        """Retrieves dictionary with dimensions of this element

        Dictionary has format like in following example: {"height": 0, "width": 0}

        :param refresh: If True, method will access web driver, otherwise returns cached value.
        :type refresh: bool
        :return: Dictionary with dimensions of this element
        :rtype: dict[int]
        """
        if refresh:
            self._logger.trace("Refreshing value of 'size' property")
            self._size = self._elem.size
            self._size["height"] = int(self._size["height"])
            self._size["width"] = int(self._size["width"])

        return self._size

    @property
    def text(self) -> str:
        """String representing the text node(s) contained by this element.

        :return: String representing the text node(s) contained by this element.
        :rtype: str
        """
        return self.get_text()

    @Wait
    def get_text(self, refresh: bool = False) -> str:
        """Retrieves string representing the text node(s) contained by this element.

        :param refresh: If True, method will access web driver, otherwise returns cached value.
        :type refresh: bool
        :return: String representing the text node(s) contained by this element.
        :rtype: str
        """
        if refresh:
            self._logger.trace("Refreshing value of element's inner text")
            self._text_node = self._elem.text

        return self._text_node

    def get_width(self, refresh: bool = False) -> int:
        """Current width of the element

        :param refresh: If True, method will access web driver, otherwise returns cached value.
        :type refresh: bool
        :return: Current width of the element
        :rtype: int
        """
        return int(self.get_size(refresh)["width"])

    def get_height(self, refresh: bool = False) -> int:
        """Current height of the element

        :param refresh: If True, method will access web driver, otherwise returns cached value.
        :type refresh: bool
        :return: Current height of the element
        :rtype: int
        """
        return int(self.get_size(refresh)["height"])

    # unstable properties that require to be queried every time
    @property
    @Wait
    def visible(self) -> bool:
        """Indicates whether or not this element is visible by user on the page

        :return: True if visible, False otherwise
        :rtype: bool
        """
        return self._elem.is_displayed()

    @property
    @Wait
    def selected(self) -> bool:
        """Indicates whether or not this element is currently selected (active) or has focus.

        :return: True if selected, False otherwise
        :rtype: bool
        """
        return self._elem.is_selected()

    @property
    @Wait
    def enabled(self) -> bool:
        """Indicates whether or not this element (usually some input or text area) is enabled and accessible.

        :return: True if enabled, False otherwise
        :rtype: bool
        """
        return self._elem.is_enabled()

    @Wait
    def get_property(self, name: str) -> str or None:
        """Retrieves specified css property value of this element.

        Almost an alias for attribute.

        :param name: Name of the element property (attribute)
        :type name: str

        :return: String representing specified css property value of this element. None if empty,
        :rtype: str | None
        """
        prop = self._elem.get_property(name)
        if prop is not None:
            prop = str(prop)

        return prop

    @Wait
    def get_attribute(self, name: str) -> str or None:
        """Retrieves value of specified attribute of this element.

        May retrieve property instead, but property is almost an alias for attribute.

        :param name: Name of the element attribute
        :type name: str

        :return: String representing value of specified attribute of this element. None if empty,
        :rtype: str | None
        """
        attr = self._elem.get_attribute(name)
        if attr is not None:
            attr = str(attr)

        return attr

    @Wait
    def get_css_property_value(self, property_name: str) -> str or None:
        """Retrieves specified css property value of this element.

        Almost an alias for attribute.

        :param property_name: Name of the css property
        :type property_name: str

        :return: String representing specified css property value of this element. None if empty,
        :rtype: str | None
        """
        css = self._elem.value_of_css_property(property_name)
        if css is not None:
            css = str(css)

        return css

    def get_inner_node(self):
        """Exposes Selenium's implementation of DOM element encapsulated by this element

        :return: Selenium internal WebElement
        :rtype: WebElement
        """
        return self._elem

    # find specific single element node passing given criteria ________________
    @Wait
    def get_element(self, selector: str, value: str) -> 'Element' or None:
        """Search for DOM element on the page by specified selector and it's value.

        If multiple elements are found to be matching given selector and its value, first one on the
        list is returned.

        :param selector: Type of the selector used for matching of wanted DOM element. One of the string constants,
            that can be found in webtest.common.selector.Selector class.
        :type selector: str
        :param value: Value of given selector type.
        :type value: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        log_message = "Searching for element by '{selector}', with '{value}'."
        self._logger.debug(log_message.format(selector=selector, value=value))
        raw_node = self._elem.find_element(selector, value)
        if not isinstance(raw_node, WebElement):
            return None

        return Element(raw_node)

    def get_element_by_id(self, id: str) -> 'Element' or None:
        """Search for DOM element on the page by ID attribute.

        :param id: ID attribute name
        :type id: str

        :return: DOM element (Node) found - i.e. new instance of MockElement with given ID
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.ID, value=id)

    def get_element_by_tag_name(self, name: str) -> 'Element' or None:
        """Search for DOM element on the page by tag name.

        If multiple elements are found to be matching the same tag name, first one on the list is returned.

        :param name: Tag name of wanted DOM element.
        :type name: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.TAG_NAME, value=name)

    def get_element_by_class_name(self, class_name: str) -> 'Element' or None:
        """Search for DOM element on the page by class name.

        If multiple elements are found to be matching the class name, first one on the list is returned.

        :param class_name: Class name of wanted DOM element.
        :type class_name: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.CLASS_NAME, value=class_name)

    def get_element_by_name_property(self, name: str) -> 'Element' or None:
        """Search for DOM element on the page by name attribute.

        If multiple elements are found to have name attribute of given value, the first one on the list is returned.

        :param name: Part of the text contained by name attribute.
        :type name: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.NAME_PROPERTY, value=name)

    def get_link_by_text(self, link_text: str) -> 'Element' or None:
        """Search for link on the page by it's text.

        If multiple links are found to be containing the same text, the first one on the list is returned.

        :param link_text: The text that wanted link is supposed to contain.
        :type link_text: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.LINK_TEXT, value=link_text)

    def get_link_by_partial_text(self, link_text: str) -> 'Element' or None:
        """Search for link on the page by part of it's text.

        If multiple links are found to be containing the same text, the first one on the list is returned.

        :param link_text: Part of the text that wanted link is supposed to contain.
        :type link_text: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.PARTIAL_LINK_TEXT, value=link_text)

    def get_element_by_xpath(self, xpath: str) -> 'Element' or None:
        """Search for DOM element on the page by XPath.

        If multiple elements are found to be matching the XPath, first one on the list is returned.

        :param xpath: XPath to the given element.
        :type xpath: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.XPATH, value=xpath)

    def get_element_by_css_selector(self, css_selector: str) -> 'Element' or None:
        """Search for DOM element on the page by css selector.

        If multiple elements are found to be matching the selector, first one on the list is returned.

        :param css_selector: Css selector matching of wanted DOM element.
        :type css_selector: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self.get_element(self, selector=Selector.CSS, value=css_selector)

    def _get_neighbour(
            self,
            tag_name: str = 'node()',
            excludes: str or list or None = 'self::text()',
            filters: str or list or None = None,
            selector: str = 'following-sibling',
            index: str or int ='1'
    ) -> 'Element' or None:
        """Get specific sibling, child or ancestor of current DOM element (node)

        Method builds based on parameters custom XPath to search for the single specific node in relation
        to the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        If even after application of all filters and excludes is there a list of nodes, the first one
        is returned.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None
        :param selector: XPath selector to further filter already selected nodes (e.g. 'following-sibling')
        :type selector: str
        :param index: XPath index to the list of selected nodes. Thanks to this XPath it self wil select
            and return one specific node.
        :type index: str | int

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: Element | None
        """
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
            index=str(index)
        )
        return self.get_element(selector=Selector.XPATH, value=xpath)

    def get_parent(self) -> 'Element' or None:
        """Get parent of current DOM element (node)

        Method builds based on parameters custom XPath to parent node of the current element.
        This is convenience method that is not part of original implementation of Selenium web driver.

        :return: Parent node of current element if any
        :rtype: Element | None
        """
        return self.get_element(selector=Selector.XPATH, value='//parent::node()')

    def get_prev_sibling(
            self,
            tag_name: str = 'node()',
            excludes: str or list or None  = 'self::text()',
            filters: str or list or None  = None
    ) -> 'Element' or None:
        """Get specific predecessor sibling of current DOM element (node)

        Method builds based on parameters custom XPath to search for the single specific sibling node
        of the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        If even after application of all filters and excludes is there a list of nodes, the first one
        is returned.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: Element | None
        """
        return self._get_neighbour(tag_name, excludes, filters, 'preceding-sibling')

    def get_next_sibling(
            self,
            tag_name: str = 'node()',
            excludes: str or list or None = 'self::text()',
            filters: str or list or None = None
    ) -> 'Element' or None:
        """Get specific following sibling of current DOM element (node)

        Method builds based on parameters custom XPath to search for the single specific sibling node
        of the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        If even after application of all filters and excludes is there a list of nodes, the first one
        is returned.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: Element | None
        """
        return self._get_neighbour(tag_name, excludes, filters, 'following-sibling')

    def get_first_child(
            self,
            tag_name: str = 'node()',
            excludes: str or list or None = 'self::text()',
            filters: str or list or None = None,
    ) -> 'Element' or None:
        """Get first possible child node of current DOM element (node) corresponding to specified parameters

        Method builds based on parameters custom XPath to search for the single specific child node
        of the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        If even after application of all filters and excludes is there a list of nodes, the first one
        is returned.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: Element | None
        """
        return self._get_neighbour(tag_name, excludes, filters, 'child')

    def get_last_child(
            self,
            tag_name: str = 'node()',
            excludes: str or list or None = 'self::text()',
            filters: str or list or None = None,
    ) -> 'Element' or None:
        """Get last possible child node of current DOM element (node) corresponding to specified parameters

        Method builds based on parameters custom XPath to search for the single specific child node
        of the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        If even after application of all filters and excludes is there a list of nodes, the first one
        is returned.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: Element | None
        """
        return self._get_neighbour(tag_name, excludes, filters, 'child', index='last()')

    # find multiple element nodes passing given criteria ______________________
    @Wait
    def get_multiple_elements(self, selector: str, value: str) -> list:
        """Search for multiple DOM elements on the page by specified selector and it's value.

        If no element is found, empty lists is returned.

        :param selector: Type of the selector used for matching of wanted DOM element. One of the string constants,
            that can be found in webtest.common.selector.Selector class.
        :type selector: str
        :param value: Value of given selector type.
        :type value: str | None

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
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

    def get_elements_by_tag_name(self, name: str) -> list:
        """Search for multiple DOM elements on the page by tag name.

        If no element is found, empty lists is returned.

        :param name: Tag name of wanted DOM element.
        :type name: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self.get_multiple_elements(self, selector=Selector.TAG_NAME, value=name)

    def get_elements_by_class_name(self, class_name: str) -> list:
        """Search for multiple DOM elements on the page by class name.

        If no element is found, empty lists is returned.

        :param class_name: Class name of wanted DOM element.
        :type class_name: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self.get_multiple_elements(self, selector=Selector.CLASS_NAME, value=class_name)

    def get_elements_by_name_property(self, name: str) -> list:
        """Search for multiple DOM elements on the page by name attribute.

        If no element is found, empty lists is returned.

        :param name: Part of the text contained by name attribute.
        :type name: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self.get_multiple_elements(self, selector=Selector.NAME_PROPERTY, value=name)

    def get_links_by_text(self, link_text: str) -> list:
        """Search for multiple links on the page by it's text.

        If no link is found, empty lists is returned.

        :param link_text: The text that wanted link is supposed to contain.
        :type link_text: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self.get_multiple_elements(self, selector=Selector.LINK_TEXT, value=link_text)

    def get_links_by_partial_text(self, link_text: str) -> list:
        """Search for multiple links on the page by part of it's text.

        If no link is found, empty lists is returned.

        :param link_text: Part of the text that wanted link is supposed to contain.
        :type link_text: str
k
        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self.get_multiple_elements(self, selector=Selector.PARTIAL_LINK_TEXT, value=link_text)

    def get_elements_by_xpath(self, xpath: str) -> list:
        """Search for multiple DOM elements on the page by XPath.

        If no element is found, empty lists is returned.

        :param xpath: XPath to the given element.
        :type xpath: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self.get_multiple_elements(self, selector=Selector.XPATH, value=xpath)

    def get_elements_by_css_selector(self, css_selector: str) -> list:
        """Search for multiple DOM elements on the page by css selector.

        If no element is found, empty lists is returned.

        :param css_selector: Css selector matching of wanted DOM element.
        :type css_selector: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self.get_multiple_elements(self, selector=Selector.CSS, value=css_selector)

    def _get_multiple_neighbours(
            self,
            tag_name: str = 'node()',
            excludes: str or list or None = 'self::text()',
            filters: str or list or None  = None,
            selector: str = 'following-sibling') -> list:
        """Get specific (sub)set of current DOM element's (node's) siblings, child nodes or "neighbours"

        Method builds based on parameters custom XPath to search for the single specific nodes in relation
        to the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None
        :param selector: XPath selector to further filter already selected nodes (e.g. 'following-sibling')
        :type selector: str

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: list[Element]
        """
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
            excludes: str or list or None = 'self::text()',
            filters: str or list or None = None
    ) -> list:
        """Get specific (sub)set of current DOM element's (node's) siblings

        Method builds based on parameters custom XPath to search for the single specific sibling nodes
        of the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: list[Element]
        """
        siblings = list()
        siblings.extend(self._get_multiple_neighbours(tag_name, excludes, filters, 'preceding-sibling'))
        siblings.extend(self._get_multiple_neighbours(tag_name, excludes, filters, 'following-sibling'))
        return siblings

    def get_child_nodes(
            self,
            tag_name: str = 'node()',
            excludes: str or list or None = 'self::text()',
            filters: str or list or None = None
    ) -> list:
        """Get specific (sub)set of current DOM element's (node's) children

        Method builds based on parameters custom XPath to search for the single specific child nodes
        of the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: list[Element]
        """
        return self._get_multiple_neighbours(tag_name, excludes, filters, 'child')

    def get_all_descendants(
            self,
            tag_name: str = 'node()',
            excludes: iter = 'self::text()',
            filters: iter or None = None
    ) -> list:
        """Get specific (sub)set of current DOM element's (node's) descendants

        Method builds based on parameters custom XPath to search for the single specific descendant nodes
        of the current element. This is convenience method that is not part of original implementation
        of Selenium web driver.

        :param tag_name: Tag name or XPath function to get list of specific types of nodes/elements
        :type tag_name: str
        :param excludes: XPath conditions that select specific elements to be excluded from selection
        :type excludes: str | list[str] | None
        :param filters: XPath conditions that select specific elements to be potentially selected and returned
        :type filters: str | list[str] | None

        :return: Element found matching the custom XPath build based on parameters supplied
        :rtype: list[Element]
        """
        return self._get_multiple_neighbours(tag_name, excludes, filters, '*')

    # perform action on element (self) ________________________________________
    # TODO: implement following methods if/when possible
    #    def location(self):
    #    def screenshot_as_base64(self):
    #    def screenshot_as_png(self):
    #    def screenshot(self, filename: str):

    @Wait
    def click(self) -> bool:
        """Method performs a mouse click on the element as actual user would in browser

        :return: True if it was possible to click on the element, False otherwise.
        :rtype: bool
        """
        self._logger.trace("Performing click on element '{}'.".format(self))
        if self.visible:
            self._elem.click()
            return True

        self._logger.trace("Element '{}' is not visible.".format(self))
        return False

    @Wait
    def type_in(self, input_text: str) -> bool:
        """Method fills the element with specified input text as actual user would in browser

        Usually can be applied to inputs and text-areas. Other types of HTML elements do not
        support this action and action will fail in such cases.

        :param input_text: Text/string to be filled into this element
        :type input_text: str

        :return: True if it was possible to fill the element with specified content, False otherwise.
        :rtype: bool
        """
        self._logger.trace("Trying to type text '{}' in element '{}'.".format(input_text, self))
        if self.visible:
            return self._elem.send_keys(input_text)

        self._logger.trace("Element '{}' is not visible.".format(self))
        return False

    @Wait
    def submit(self) -> bool:
        """Method tries to submit form that has some relation to this element

        Method tries to locate ancestor "form" element and it's submit button.
        Method is implemented entirely by the Selenium it self and there is no
        guarantee for it to work, as one might expect.

        :return: True if it was possible to click on the element, False otherwise.
        :rtype: bool
        """
        self._logger.trace("Trying to perform 'submit' on element '{}'.".format(self))
        if self.visible:
            return self._elem.submit()

        self._logger.trace("Element '{}' is not visible.".format(self))
        return False

    @Wait
    def clear(self) -> bool:
        """Method fills the element with specified input text as actual user would in browser

        Usually can be applied to inputs and text-areas. Other types of HTML elements do not
        support this action and action will fail in such cases. Will fail on selects.

        :return: True if it was possible to fill the element with specified content, False otherwise.
        :rtype: bool
        """
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
        """Method scrolls wit the page to move element can be visible for user in browser window

        It is not correctly supported by all the WebDrivers/browsers so ti will currently always fail.
        (i.e. method is not properly implemented)

        :return: True if it was possible to fill the element with specified content, False otherwise.
        :rtype: bool
        """
        self._logger.trace("Trying to check visibility and scroll element '{}' into view.".format(self))
        # TODO: implement this method
        # location_once_scrolled_into_view():
        return False

    # perform action on element that is supposed to be component of form (self)
    def fill(self, value: tuple or list or str) -> bool:
        """Method that fills (or attempts to do so) given value to this element

        Based on the data structure supplied and based on type of this element, method tries
        to select correct fill_*() method for this element.

        :param value: Input data, that should correspond to signatures of other fill_*() methods for Element class.
        :type value: str | tuple[str] | list[str]

        :return: Indication of success - True if filled correctly, False otherwise
        :rtype: bool
        """
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
        """Method that fills (or attempts to do so) all descendant elements with input data

        Method assumes that this element is <form> or <div> contained by <form> (or similar situation)
        and based on list of input data tries to locate corresponding descendant elements and fill them
        with the correct input form supplied values. Content of the list should by tuples or lists
        matching signatures of other fill_*() methods for Element class.

        :param items: List of input data, that should correspond to signatures of other fill_*() methods
            for Element class.
        :type items: list

        :return: Indication of success - True if all descendants were filled correctly, False otherwise
        :rtype: bool
        """
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
        """Method that fills (or attempts to do so) given value to this element if it is <input> element

        This element must be correct input type and have correct name (if any).

        :param data: tuple or list with 2 or 3 members corresponding to following information:
            input attribute *type*, *value* to be filled and *name* attribute which is optional
            value can be boolean (bool) if this is a check-box or radio-button
        :type data: tuple[str] | list[str]

        :return: Indication of success - True if filled correctly, False otherwise
        :rtype: bool
        """
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

        if self.get_attribute(self, 'type') != input_type:
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
        """Method tries to find and select given options, if this is <select> type element

        :param options: List of strings representing the individual options to select as they would be visible
            to the actual user.
        :type options: list[str]

        :return: Indication of success - True if filled correctly, False otherwise
        :rtype: bool
        """
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
        """Method will fill this element with given data, if this element is text area

        If this element is not a text area, method attempts anyway, but there is high likelihood of failure.

        :param data: data to be filled into this element
        :type data: str | list[str] tuple[str]

        :return: Indication of success - True if filled correctly, False otherwise
        :rtype: bool
        """
        if self.tag_name != 'textarea':
            self._logger.warning("Attempt to act as if <{}> was <textarea> element".format(self.tag_name))

        if not self.visible:
            self._logger.trace("Element '{}' is not visible.".format(self))
            return False

        self.clear(self)
        if not isinstance(data, str):
            text = "\n".join(list(data))
        else:
            text = data
        return self.type_in(text)
