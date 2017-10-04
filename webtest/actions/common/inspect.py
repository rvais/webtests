#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import logging
from time import sleep

from webtest.common.logger import get_logger
from webtest.webagent import WebAgent
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.component import Component
from webtest.components.pagemodel.element import Element
from webtest.common.scripts.frameworks import angular_loaded, render_cycle
from webtest.actions.user_action import UserAction

class Inspect(UserAction):
    def __init__(self, expect: object=False,  *args, **kwargs):
        super(Inspect, self).__init__(*args, **kwargs)
        self._expected = expect
        self._redirection = False
        self._failure_msg = "Nothing to inspect"
        self._perform_msg = "Performing check of content ({}).".format(self.name)


    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info(self._perform_msg)
        exception = None
        try:
            check = self._expected == self._inspect(agent)
        except Exception as ex:
            exception = ex
            check = False

        result = True

        if check != self._expected or exception is not None:
            self.action_failure(ex=exception, msg=self._failure_msg)
            self._logger.warning("expected = '{}'".format(self._expected))
            self._logger.warning("gained = '{}'".format(check))
            result = False

        return result


    def _inspect(self, agent: 'WebAgent') -> object:
        raise Exception("This is abstract class, subclass has to redefine _inspect() method.")



class CheckURL(Inspect):
    def __init__(self, *args, **kwargs):
        super(CheckURL, self).__init__(*args, **kwargs)
        self._failure_msg = "Url gained does not equal to expected one."
        self._perform_msg = "Performing url check."


    def _inspect(self, agent: 'WebAgent') -> object:
        page = agent.get_current_page()
        return page.url



class ComponentExists(Inspect):
    def __init__(self, component_name: str=Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(ComponentExists, self).__init__(True, **kwargs)
        self._failure_msg = "HTML element of specified component does not exist on currently visited page."
        self._perform_msg = "Performing searching for HTML element of '{}' component.".format(component_name)

        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))


    def _inspect(self, agent: 'WebAgent') -> object:
        page = agent.get_current_page()  # type: Page
        component = UserAction._get_component(page, self._component, self._subcomponents)
        return component is not None



class LinkExists(Inspect):
    def __init__(self, link_text:str, component_name: str=Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(LinkExists, self).__init__(**kwargs)
        self._failure_msg = "Hypertext link with given text does not exist under specified component on currently visited page."
        self._perform_msg = "Performing searching for hypertext link with text '{}' under '{}'component.".format(link_text, component_name)

        self._link_text = link_text
        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))


    def _inspect(self, agent: 'WebAgent') -> object:
        page = agent.get_current_page()  # type: Page
        link = UserAction._get_link_first_visible(page, self._link_text, self._component, self._subcomponents)
        return link is not None



class ElementContentText(Inspect):
    def __init__(self, text_content: str, selector: str, value: str, component_name: str=Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(ElementContentText, self).__init__(True, **kwargs)
        self._failure_msg = "Content of specified element differs from expected value."
        self._perform_msg = "Performing content check."

        self._content = text_content
        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))


    def _inspect(self, agent: 'WebAgent') -> object:
        page = agent.get_current_page()  # type: Page
        element = UserAction._get_element(
            page, self._selector, self._selector_value, self._component, self._subcomponents) # type: Element

        if element is None:
            return False

        return element.text.find(self._content) >= 0

# class GenericCheck(Inspect):
#     def __init__(self, *args, **kwargs):
#         super(GenericCheck, self).__init__(True, *args, **kwargs)
#         self._failure_msg = "Nothing to check, it's generic so nothing happened."
#         self._perform_msg = "Performing generic check, that is going to fail."
#
#     def _inspect(self, agent: 'WebAgent') -> object:
#         return False


