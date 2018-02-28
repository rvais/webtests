#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.mock_element import MockElement
from webtest.components.pagemodel.element import Element
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


# noinspection PyMissingConstructor
class MockDriver(WebDriver):
    """Class overriding original Selenium WebDriver for debugging and experimental purposes.

    This class is useful only in case you want to test/mock framework capabilities, new functionality
    or debug it's issues without need for actually launching web driver and browser.
    """

    def __init__(self):
        self._mockelem = MockElement("mockelement")

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (session="{1}")>'.format(
            type(self), self.session_id)

    @property
    def mobile(self):
        """Indicates whether browser is from mobile device or computer

        :return: Always False - i.e. imaginary browser is always on the computer
        :rtype: bool
        """
        return False

    @property
    def name(self):
        """Name of imaginary browser this web driver is hooked on

        :return: Name of imaginary browser this web driver is hooked on.
        :rtype: str
        """
        return "Mock of a browser"

    def start_session(self, capabilities, browser_profile=None):
        """Start new session in the selected browser with given desired capabilities.

        No selenium is employed here so there is also no session to start. Only to override original interface.
        Passed arguments are ignored.

        :param capabilities:
        :type capabilities:
        :param browser_profile:
        :type browser_profile:
        """
        pass

    def _wrap_value(self, value):
        """Wrap the value for selenium web driver

        No selenium is employed here so there is also nothing to wrap. Only to override original interface.

        :param value: Value to unwrap
        :type value: object

        :return: Passed value
        :rtype: object
        """
        return value

    def create_web_element(self, element_id: str) -> MockElement:
        """Creates new DOM element, that is located on imaginary page.

        Method serves to override original interface. Creates MockElement. ID here represents something different
        than ID in original web driver, where ID is unique internal identifier for that specific node.

        :param element_id: Text of ID attribute of the DOM element. Differs form original web driver
        :type element_id: str

        :return: New instance of MockElement
        :rtype: MockElement
        """
        return MockElement("mockelement", element_id)

    def _unwrap_value(self, value):
        """Unwrap the value returned by selenium.

        No selenium is employed here so there is also nothing to unwrap. Only to override original interface.

        :param value: Value to unwrap
        :type value: object

        :return: Passed value
        :rtype: object
        """
        return value

    def execute(self, driver_command, params=None):
        """Executes given command in imaginary web browser

        :param driver_command: Command to be executed. Ignored!
        :type driver_command: object
        :param params: List (or something) of arguments for command to be executed. Ignored!
        :type params: object | None

        :return: Static empty successful result
        :rtype: dict
        """
        return {'success': 0, 'value': None, 'sessionId': 42}

    def get(self, url: str):
        """Visit the page that has given URL address.

        It is an empty action. Argument is ignored and nothing happens.

        :param url: URL address that can be normally found in address bar of your browser.
        :type url: str
        """
        pass

    @property
    def title(self):
        """Title of currently opened page.

        :return: Title of currently opened page. Static string.
        :rtype: str
        """
        return "Mock title"

    def find_element_by_id(self, id_: str) -> Element or None:
        """Search for DOM element on the page by ID attribute.

        :param id_: ID attribute name
        :type id_: str

        :return: DOM element (Node) found - i.e. new instance of MockElement with given ID
        :rtype: Element | None
        """
        return self.create_web_element(id_)

    def find_elements_by_id(self, id_: str) -> list:
        """Search for multiple DOM elements on the page by ID attribute.

        This method is there just as "convention" that other find_element_* methods follow (and because
        it is in original WebDriver class). Page should never contain two or more elements with the same ID.

        :param id_: ID attribute name
        :type id_: str

        :return: list with DOM elements (Nodes) found - i.e. list with new instance of MockElement with given ID
        :rtype: list[Element]
        """
        return [self.create_web_element(id_)]

    def find_element_by_xpath(self, xpath: str) -> Element or None:
        """Search for DOM element on the page by XPath.

        If multiple elements are found to be matching the XPath, first one on the list is returned.

        :param xpath: XPath to the given element.
        :type xpath: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem.get_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath: str) -> list:
        """Search for multiple DOM elements on the page by XPath.

        If no element is found, empty lists is returned.

        :param xpath: XPath to the given element.
        :type xpath: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self._mockelem.get_elements_by_xpath(xpath)

    def find_element_by_link_text(self, link_text: str) -> Element or None:
        """Search for link on the page by it's text.

        If multiple links are found to be containing the same text, the first one on the list is returned.

        :param link_text: The text that wanted link is supposed to contain.
        :type link_text: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem.get_link_by_text(link_text)

    def find_elements_by_link_text(self, text: str) -> list:
        """Search for multiple links on the page by it's text.

        If no link is found, empty lists is returned.

        :param text: The text that wanted link is supposed to contain.
        :type text: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self._mockelem.get_links_by_text(text)

    def find_element_by_partial_link_text(self, link_text: str) -> Element or None:
        """Search for link on the page by part of it's text.

        If multiple links are found to be containing the same text, the first one on the list is returned.

        :param link_text: Part of the text that wanted link is supposed to contain.
        :type link_text: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem.get_link_by_partial_text(link_text)

    def find_elements_by_partial_link_text(self, link_text: str) -> list:
        """Search for multiple links on the page by part of it's text.

        If no link is found, empty lists is returned.

        :param link_text: Part of the text that wanted link is supposed to contain.
        :type link_text: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self._mockelem.get_links_by_partial_text(link_text)

    def find_element_by_name(self, name: str) -> Element or None:
        """Search for DOM element on the page by name attribute.

        If multiple elements are found to have name attribute of given value, the first one on the list is returned.

        :param name: Part of the text contained by name attribute.
        :type name: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem.get_element_by_name_property(name)

    def find_elements_by_name(self, name: str) -> list:
        """Search for multiple DOM elements on the page by name attribute.

        If no element is found, empty lists is returned.

        :param name: Part of the text contained by name attribute.
        :type name: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self._mockelem.get_elements_by_name_property(name)

    def find_element_by_tag_name(self, name: str) -> Element or None:
        """Search for DOM element on the page by tag name.

        If multiple elements are found to be matching the same tag name, first one on the list is returned.

        :param name: Tag name of wanted DOM element.
        :type name: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem.get_element_by_tag_name(name)

    def find_elements_by_tag_name(self, name: str) -> list:
        """Search for multiple DOM elements on the page by tag name.

        If no element is found, empty lists is returned.

        :param name: Tag name of wanted DOM element.
        :type name: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self._mockelem.get_elements_by_tag_name(name)

    def find_element_by_class_name(self, name: str) -> Element or None:
        """Search for DOM element on the page by class name.

        If multiple elements are found to be matching the class name, first one on the list is returned.

        :param name: Class name of wanted DOM element.
        :type name: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem.get_element_by_class_name(name)

    def find_elements_by_class_name(self, name: str) -> list:
        """Search for multiple DOM elements on the page by class name.

        If no element is found, empty lists is returned.

        :param name: Class name of wanted DOM element.
        :type name: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self._mockelem.get_elements_by_class_name(name)

    def find_element_by_css_selector(self, css_selector: str) -> Element or None:
        """Search for DOM element on the page by css selector.

        If multiple elements are found to be matching the selector, first one on the list is returned.

        :param css_selector: Css selector matching of wanted DOM element.
        :type css_selector: str

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem.get_element_by_css_selector(css_selector)

    def find_elements_by_css_selector(self, css_selector: str) -> list:
        """Search for multiple DOM elements on the page by css selector.

        If no element is found, empty lists is returned.

        :param css_selector: Css selector matching of wanted DOM element.
        :type css_selector: str

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        return self._mockelem.get_elements_by_css_selector(css_selector)

    def find_element(self, by: str = By.ID, value: str or None = None) -> Element or None:
        """Search for DOM element on the page by specified selector and it's value.

        If multiple elements are found to be matching given selector and its value, first one on the
        list is returned.

        :param by: Type of the selector used for matching of wanted DOM element. One of the string constants,
            that can be found in webtest.common.selector.Selector class.
        :type by: str
        :param value: Value of given selector type.
        :type value: str | None

        :return: DOM element (Node) found - i.e. instance of MockElement - or None
        :rtype: Element | None
        """
        return self._mockelem

    def find_elements(self, by: str = By.ID, value: str or None = None) -> list:
        """Search for multiple DOM elements on the page by specified selector and it's value.

        If no element is found, empty lists is returned.

        :param by: Type of the selector used for matching of wanted DOM element. One of the string constants,
            that can be found in webtest.common.selector.Selector class.
        :type by: str
        :param value: Value of given selector type.
        :type value: str | None

        :return: list of DOM elements (Nodes) - i.e. instances of MockElement - found
        :rtype: list[Element]
        """
        l = list()
        l.append(self._mockelem)
        return l

    @property
    def current_url(self) -> str:
        """URL address of currently visited page.

        :return: URL address for imaginary example page.
        :rtype: str
        """
        return "http://www.example.com/404.html"

    @property
    def page_source(self) -> str:
        """Source HTML code of the imaginary website.

        :return: Always an empty string
        :rtype: str
        """
        return ""

    def close(self) -> None:
        """Closes current window of the web browser linked to this driver and this session (NOP)"""
        pass

    def quit(self) -> None:
        """Exits the web browser linked to this driver and this session (NOP)"""
        pass

    # noinspection PyPropertyDefinition
    @property
    def current_window_handle(self) -> object or None:
        return None

    # noinspection PyPropertyDefinition
    @property
    def window_handles(self) -> object or None:
        """Returns handle object of currently opened window

        :return: None
        :rtype: object | None
        """
        return None

    def maximize_window(self):
        """Maximizes the window of the currently running browser (NOP)"""
        pass

    # noinspection PyPropertyDefinition
    @property
    def switch_to(self) -> object or None:
        """Some object replacing some of the methods (Target Locators below) in original WebDriver

        In this case, returns always None

        :return: None
        :rtype: object | None
        """
        return None

    # Target Locators
    def switch_to_active_element(self):
        pass

    def switch_to_window(self, window_name):
        pass

    def switch_to_frame(self, frame_reference):
        pass

    def switch_to_default_content(self):
        pass

    def switch_to_alert(self):
        return None

    # Navigation
    def back(self):
        pass

    def forward(self):
        pass

    def refresh(self):
        pass

    # Options
    def get_cookies(self):
        return None

    def get_cookie(self, name):
        return None

    def delete_cookie(self, name):
        pass

    def delete_all_cookies(self):
        pass

    def add_cookie(self, cookie_dict):
        pass

    # Timeouts
    def implicitly_wait(self, time_to_wait):
        pass

    def set_script_timeout(self, time_to_wait):
        pass

    def set_page_load_timeout(self, time_to_wait):
        pass

    # noinspection PyPropertyDefinition
    @property
    def desired_capabilities(self):
        return None

    def get_screenshot_as_file(self, filename):
        return False

    def save_screenshot(self, filename):
        return None

    def get_screenshot_as_png(self):
        return None

    def get_screenshot_as_base64(self):
        return None

    def set_window_size(self, width, height, windowHandle='current'):
        pass

    def get_window_size(self, windowHandle='current'):
        return None

    def set_window_position(self, x, y, windowHandle='current'):
        pass

    def get_window_position(self, windowHandle='current'):
        return None

    def get_window_rect(self):
        return None

    def set_window_rect(self, x=None, y=None, width=None, height=None):
        pass

    @property
    def file_detector(self):
        return None

    @file_detector.setter
    def file_detector(self, detector):
        pass

    @property
    def orientation(self):
        return None

    @orientation.setter
    def orientation(self, value):
        pass

    @property
    def application_cache(self):
        return None

    @property
    def log_types(self):
        return None

    def get_log(self, log_type):
        return ""
