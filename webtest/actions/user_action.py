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

class UserAction(object):
    def __init__(self):
        self._class_name = str(self.__class__.__name__)
        self._logger = get_logger(self._class_name) # type: logging.Logger

        self._redirection = False
        self._change = False
        self._delay_for_user = True

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Performing generic user action.")
        return True

    def action_failure(self, ex: Exception=None, msg: str=None ):
        self._logger.info("Action '{}' FAILED.".format(self._class_name))
        if msg is not None:
            self._logger.info(msg)

        if ex is not None:
            self._logger.warning(ex)

    def expected_redirection(self) -> bool:
        return self._redirection

    def expected_content_change(self) -> bool:
        return self._change

    def delay_for_user_to_see(self) -> bool:
        return self._delay_for_user

    def set_expected_redirection(self, redirection: bool):
        self._redirection = redirection

    def set_expected_content_change(self, change: bool):
        self._change = change

    def set_delay_active(self, do_delay: bool):
        self._delay_for_user = do_delay

    def wait_for_frameworks(self, agent: 'WebAgent') -> None:
        page = agent.get_current_page()
        page.execute_script(render_cycle, False)
        sleep(2)
        page.execute_script(angular_loaded)


    @staticmethod
    def _get_component(page: Page, component: str, subcomponents: list) -> Component or None:
        component = page.get_component(component) # type: Component

        if len(subcomponents) > 0 and component is not None:
            subcomponent = component # type: Component
            for component_name in subcomponents:
                subcomponent = subcomponent.get_subcomponent(component_name)
                if subcomponent is None:
                    break

            component = subcomponent

        return component

    @staticmethod
    def _get_element(
            page: Page,
            selector: str,
            value: str,
            component: str=Page.ROOT_COMPONENT_NAME,
            subcomponents: list=list()
    ) -> Element or None:
        component = UserAction._get_component(page, component, subcomponents)
        if component is None:
            return component

        node = component.get_element_node()
        return node.get_element(selector, value)

    @staticmethod
    def _get_link(
            page: Page,
            text: str,
            component: str=Page.ROOT_COMPONENT_NAME,
            subcomponents: list=list()
    ) -> Element or None:
        component = UserAction._get_component(page, component, subcomponents)
        if component is None:
            return component

        node = component.get_element_node()
        return node.get_link_by_partial_text(text)

class FindComponent(UserAction):
    def __init__(self, component_name: str=Page.ROOT_COMPONENT_NAME, *args):
        super(FindComponent, self).__init__()

        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> Component or None:
        page = agent.get_current_page()  # type: Page
        try:
            component = UserAction._get_component(page, self._component, self._subcomponents)
            self._logger.info("Searching for component '{}'.".format(component.name))
            return component

        except Exception as ex:
            self.action_failure()
            return None



class FindLink(UserAction):
    def __init__(self, link_text:str, component_name: str=Page.ROOT_COMPONENT_NAME, *args):
        super(FindLink, self).__init__()

        self._component = component_name
        self._subcomponents = list()
        self._link_text = link_text
        if len(args) > 0:
            self._subcomponents.extend(list(args))


    def perform_self(self, agent: 'WebAgent') -> Element or None:
        page = agent.get_current_page()  # type: Page
        try:
            link = UserAction._get_link(page, self._link_text, self._component, self._subcomponents)
            self._logger.info("Searching for link with text '{}'.".format(self._link_text))
            return link

        except Exception as ex:
            self.action_failure(ex)
            return None



class FindElement(UserAction):
    def __init__(self, selector: str, value: str, component_name: str=Page.ROOT_COMPONENT_NAME, *args):
        super(FindElement, self).__init__()

        self._component = component_name
        self._subcomponents = list()
        self._selector = selector
        self._selector_value = value
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> Element or None:
        page = agent.get_current_page()  # type: Page
        try:
            self._logger.info("Searching for element by selector '{}' "
                              "with value '{}' .".format(self._selector, self._selector_value))

            element = UserAction._get_element(
                page, self._selector, self._selector_value, self._component, self._subcomponents)
            return element

        except Exception as ex:
            self.action_failure(ex)
            return None