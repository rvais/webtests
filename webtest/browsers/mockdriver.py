#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.mock_element import MockElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class MockDriver(WebDriver):

    def __init__(self):
        self._mockelem = MockElement("mockelement")

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (session="{1}")>'.format(
            type(self), self.session_id)

    @property
    def mobile(self):
        return False

    @property
    def name(self):
        return "Mock of a browser"

    def start_session(self, capabilities, browser_profile=None):
        pass

    def _wrap_value(self, value):
        return value

    def create_web_element(self, element_id):
        return MockElement("mockelement", element_id)

    def _unwrap_value(self, value):
        return value

    def execute(self, driver_command, params=None):
        return {'success': 0, 'value': None, 'sessionId': 42}

    def get(self, url):
        pass

    @property
    def title(self):
        return "Mock title"

    def find_element_by_id(self, id_):
        return self.create_web_element(id_)

    def find_elements_by_id(self, id_):
        return self.create_web_element(id_).find_element_by_id(id_);

    def find_element_by_xpath(self, xpath):
        return self._mockelem.find_element_by_xpath(xpath)


    def find_elements_by_xpath(self, xpath):
        return self._mockelem.find_elements_by_xpath(xpath)

    def find_element_by_link_text(self, link_text):
        return self._mockelem.find_element_by_link_text(link_text)

    def find_elements_by_link_text(self, text):
        return self._mockelem.find_elements_by_link_text(text)

    def find_element_by_partial_link_text(self, link_text):
        return self._mockelem.find_elements_by_partial_link_text(link_text)

    def find_elements_by_partial_link_text(self, link_text):
        return self._mockelem.find_elements_by_partial_link_text(link_text)

    def find_element_by_name(self, name):
        return self._mockelem.find_element_by_name(name)

    def find_elements_by_name(self, name):
        return self._mockelem.find_elements_by_name(name)

    def find_element_by_tag_name(self, name):
        return self._mockelem.find_element_by_tag_name(name)

    def find_elements_by_tag_name(self, name):
        return self._mockelem.find_elements_by_tag_name(name)

    def find_element_by_class_name(self, name):
        return self._mockelem.find_element_by_class_name(name)

    def find_elements_by_class_name(self, name):
        return self._mockelem.find_elements_by_class_name(name)

    def find_element_by_css_selector(self, css_selector):
        return self._mockelem.find_element_by_css_selector(css_selector)

    def find_elements_by_css_selector(self, css_selector):
        return self._mockelem.find_element_by_css_selector(css_selector)

    @property
    def current_url(self):
        return "http://www.example.com/404.html"

    @property
    def page_source(self):
        return ""

    def close(self):
        pass

    def quit(self):
        pass

    @property
    def current_window_handle(self):
        None

    @property
    def window_handles(self):
        None

    def maximize_window(self):
        pass

    @property
    def switch_to(self):
        pass

    # Target Locators
    def switch_to_active_element(self):
        return None

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

    def find_element(self, by=By.ID, value=None):
        return self._mockelem

    def find_elements(self, by=By.ID, value=None):
        l = list()
        l.append(self._mockelem)
        return l

    @property
    def desired_capabilities(self):
        None

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
