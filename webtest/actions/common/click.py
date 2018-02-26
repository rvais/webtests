#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.element import Element
from webtest.components.pagemodel.component import Component

# Group of actions dedicated to clicking on things on a web page.

#
# Action performing click on a known part of web page. Such part is usually
# as component in a template for given page and is expected to exist.
#
class ClickOnComponent(UserAction):
    # Strings representing hierarchy of components are expected as positional arguments.
    def __init__(self, component_name: str=Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(ClickOnComponent, self).__init__(**kwargs)

        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> bool:
        page = agent.get_current_page()  # type: Page
        try:
            component = UserAction._get_component(page, self._component, self._subcomponents) # type: Component
            if component.visible:
                self._logger.info("Clicking on component '{}'.".format(component.name))
                return component.click()
            else:
                self._action_failure(msg="Component is not visible.")
                return False

        except BaseException as ex:
            self._action_failure()
            return False


#
# Action performing click on a link found by its text. Search is performed
# on some component known in a template for given page and is expected to exist.
#
class ClickOnLink(UserAction):
    # Link text followed by strings representing hierarchy of components are expected as positional arguments.
    def __init__(self, link_text:str, component_name: str=Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(ClickOnLink, self).__init__(**kwargs)

        self._redirection = True if 'redirection' not in kwargs else self._redirection
        self._change = True if 'page_change' not in kwargs else self._change

        self._component = component_name
        self._subcomponents = list()
        self._link_text = link_text
        if len(args) > 0:
            self._subcomponents.extend(list(args))


    def perform_self(self, agent: 'WebAgent') -> bool:
        page = agent.get_current_page()  # type: Page
        try:
            self._logger.debug("Attempt to click on link with text '{}'.".format(self._link_text))
            link = UserAction._get_link(page, self._link_text, self._component, self._subcomponents) # type: Element
            if link.visible:
                self._logger.info("Clicking on link with text '{}'.".format(self._link_text))
                return link.click(link)
            else:
                self._action_failure(msg="Element is not visible.")
                return False

        except BaseException as ex:
            self._action_failure(ex)
            return False

#
# Exactly the same as ClickOnLink but with slightly different implementation
# of searching for link it self.
#
class ClickOnLinkFirstVisible(ClickOnLink):
    def __init__(self, *args, **kwargs):
        super(ClickOnLinkFirstVisible, self).__init__(*args,**kwargs)

    def perform_self(self, agent: 'WebAgent') -> bool:
        page = agent.get_current_page()  # type: Page
        try:
            self._logger.debug("Attempt to click on link with text '{}'.".format(self._link_text))
            link = UserAction._get_link_first_visible(page, self._link_text, self._component, self._subcomponents) # type: Element
            if link.visible:
                self._logger.info("Clicking on link with text '{}'.".format(self._link_text))
                return link.click(link)
            else:
                self._action_failure(msg="Element is not visible.")
                return False

        except BaseException as ex:
            self._action_failure(ex)
            return False


#
# Action performing click on a any element found in website. Search is performed
# on some component known in a template for given page and is expected to exist.
#
class ClickOnElement(UserAction):
    # Type of element selector with its value followed by strings representing
    # hierarchy of components are expected as positional arguments.
    def __init__(self, selector: str, value: str, component_name: str=Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(ClickOnElement, self).__init__(**kwargs)

        self._component = component_name
        self._subcomponents = list()
        self._selector = selector
        self._selector_value = value
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> bool:
        page = agent.get_current_page()  # type: Page
        try:
            element = UserAction._get_element(
                page, self._selector, self._selector_value, self._component, self._subcomponents) # type: Element

            if element.visible:
                self._logger.info("Clicking on element searched by selector '{}' "
                                  "with value '{}' .".format(self._selector, self._selector_value))
                return element.click(element)
            else:
                self._action_failure(msg="Element is not visible.")
                return False

        except BaseException as ex:
            self._action_failure(ex)
            return False