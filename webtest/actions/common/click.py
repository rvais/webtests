#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
"""Group of actions dedicated to clicking on things on a web page."""

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.element import Element
from webtest.components.pagemodel.component import Component


class ClickOnComponent(UserAction):
    """Specific UserAction class. Action performing click on a known element of web page, represented by component.

    Component is usually defined in a template for given page and is expected to exist.
    """

    def __init__(self, component_name: str = Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        """Constructor is responsible for initializing instance and common attributes shared by all user actions.

        :param component_name: Name of the component as defined in model to be searched for.
        :type component_name: str
        :param args: List of component names in order as they are nested in page model. These names represent
            path to component that is supposed to contain wanted component. DO NOT pass as list but RATHER individual
            strings. These will be packed into the list/tuple by python itself.
        :param type: list | tuple
        :param description: Documentation string of this specific instance user action. (Test documentation)
        :type description: str
        :param expected_result: Documentation string of expected outcome / consequences of this specific instance
            of user action. (Test documentation)
        :type expected_result: str
        :param redirection: Indicates whether or not should be page redirected as a consequence of this action
        :type redirection: bool
        :param page_change: Indicates whether or not should page change its content as a consequence of this action
        :type page_change: bool
        :param delay: Explicit delay, before next action may start its execution. Default is 0
        :type delay: int
        :param stop_on_failure: Indicates whether or not will scenario execution stop if action fail. Default True
        :type stop_on_failure: bool
        """
        super(ClickOnComponent, self).__init__(**kwargs)

        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> bool:
        page = agent.get_current_page()  # type: Page
        try:
            component = UserAction._get_component(page, self._component, self._subcomponents)  # type: Component
            if component.visible:
                self._logger.info("Clicking on component '{}'.".format(component.name))
                return component.click()
            else:
                self._action_failure(msg="Component is not visible.")
                return False

        except BaseException as ex:
            self._action_failure(ex)
            return False


#
# Action performing click on a link found by its text. Search is performed
# on some component known in a template for given page and is expected to exist.
#
class ClickOnLink(UserAction):
    """Specific UserAction class. Action performing click on a known link of web page."""

    # Link text followed by strings representing hierarchy of components are expected as positional arguments.
    def __init__(self, link_text: str, component_name: str = Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        """Constructor is responsible for initializing instance and common attributes shared by all user actions.

        :param component_name: Name of the component as defined in model to be searched for.
        :type component_name: str
        :param args: List of component names in order as they are nested in page model. These names represent
            path to component that is supposed to contain wanted component. DO NOT pass as list but RATHER individual
            strings. These will be packed into the list/tuple by python itself.
        :param type: list | tuple
        :param description: Documentation string of this specific instance user action. (Test documentation)
        :type description: str
        :param expected_result: Documentation string of expected outcome / consequences of this specific instance
            of user action. (Test documentation)
        :type expected_result: str
        :param redirection: Indicates whether or not should be page redirected as a consequence of this action
        :type redirection: bool
        :param page_change: Indicates whether or not should page change its content as a consequence of this action
        :type page_change: bool
        :param delay: Explicit delay, before next action may start its execution. Default is 0
        :type delay: int
        :param stop_on_failure: Indicates whether or not will scenario execution stop if action fail. Default True
        :type stop_on_failure: bool
        """
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
            link = UserAction._get_link(page, self._link_text, self._component, self._subcomponents)  # type: Element
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
    """Specific UserAction class. Action performing click on a known link of web page.

    Exactly the same as ClickOnLink but with slightly different implementation of searching for link it self.
    """

    def __init__(self, *args, **kwargs):
        """Constructor is responsible for initializing instance and common attributes shared by all user actions.

        :param link_text: Expected text that user would see in web page.
        :type link_text: str
        :param component_name: Name of the component as defined in model to be used .
        :type component_name: str
        :param args: List of component names in order as they are nested in page model. These names represent
            path to component that is supposed to contain wanted component. DO NOT pass as list but RATHER individual
            strings. These will be packed into the list/tuple by python itself.
        :type: list | tuple
        :param description: Documentation string of this specific instance user action. (Test documentation)
        :type description: str
        :param expected_result: Documentation string of expected outcome / consequences of this specific instance
            of user action. (Test documentation)
        :type expected_result: str
        :param redirection: Indicates whether or not should be page redirected as a consequence of this action
        :type redirection: bool
        :param page_change: Indicates whether or not should page change its content as a consequence of this action
        :type page_change: bool
        :param delay: Explicit delay, before next action may start its execution. Default is 0
        :type delay: int
        :param stop_on_failure: Indicates whether or not will scenario execution stop if action fail. Default True
        :type stop_on_failure: bool
        """
        super(ClickOnLinkFirstVisible, self).__init__(*args, **kwargs)

    def perform_self(self, agent: 'WebAgent') -> bool:
        page = agent.get_current_page()  # type: Page
        try:
            self._logger.debug("Attempt to click on link with text '{}'.".format(self._link_text))
            link = UserAction._get_link_first_visible(page, self._link_text, self._component,
                                                      self._subcomponents)  # type: Element
            if link.visible:
                self._logger.info("Clicking on link with text '{}'.".format(self._link_text))
                return link.click(link)
            else:
                self._action_failure(msg="Element is not visible.")
                return False

        except BaseException as ex:
            self._action_failure(ex)
            return False


class ClickOnElement(UserAction):
    """Specific UserAction class. Action performing click on a known DOM element of web page.

    Search fot DOM element is performed on some component known in a template for given page and is expected to exist.
    """

    def __init__(self, selector: str, value: str, component_name: str = Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        """Constructor is responsible for initializing instance and common attributes shared by all user actions.

        :param selector: Selector type constant, attribute of webtest.common.selector.Selector
        :type selector: str
        :param value: Value of the selector
        :type value: str
        :param component_name: Name of the component as defined in model to be searched for.
        :type component_name: str
        :param args: List of component names in order as they are nested in page model. These names represent
            path to component that is supposed to contain wanted component. DO NOT pass as list but RATHER individual
            strings. These will be packed into the list/tuple by python itself.
        :param type: list | tuple
        :param description: Documentation string of this specific instance user action. (Test documentation)
        :type description: str
        :param expected_result: Documentation string of expected outcome / consequences of this specific instance
            of user action. (Test documentation)
        :type expected_result: str
        :param redirection: Indicates whether or not should be page redirected as a consequence of this action
        :type redirection: bool
        :param page_change: Indicates whether or not should page change its content as a consequence of this action
        :type page_change: bool
        :param delay: Explicit delay, before next action may start its execution. Default is 0
        :type delay: int
        :param stop_on_failure: Indicates whether or not will scenario execution stop if action fail. Default True
        :type stop_on_failure: bool
        """
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
                page, self._selector, self._selector_value, self._component, self._subcomponents)  # type: Element

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
