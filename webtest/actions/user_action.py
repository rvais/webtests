#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import logging
from time import sleep

from webtest.common.logging.logger import get_logger
from webtest.common.selector import Selector
from webtest.webagent import WebAgent
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.component import Component
from webtest.components.pagemodel.element import Element
from webtest.common.scripts.frameworks import angular_loaded, render_cycle


class UserAction(object):
    """UserAction class represents abstraction of each possible action that user
    Can perform and by doing so interact with webpage in his browser. Class
    contains implementation of methods that are common for every action form
    test's and background code's point of view. Also has support methods for
    its subclasses. To create new user action this class needs to be subclassed,
    methods __init__() and perform_self() overridden.
    """

    def __init__(self, description: str or None = None, expected_result: str or None = None, redirection: bool = False,
                 page_change: bool = False, delay: int = 0, stop_on_failure: bool = True):
        """Constructor. Method is responsible for initializing common attributes shared by all user actions.

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
        self._class_name = str(self.__class__.__name__)
        self._logger = get_logger(self._class_name)  # type: logging.Logger

        self._description = description
        if not description:
            self._description = "Perform generic user action."

        self._expected = expected_result
        if not expected_result:
            self._expected = "No error should occur and no exceptions should be raised during execution."

        self._redirection = redirection
        self._change = page_change
        self._delay_for_user = delay
        self._stop_on_failure = stop_on_failure

        self._success = None
        self._ex = None
        self._failure = "Action '{}' haven't been executed yet.".format(self._class_name)

    def perform_self(self, agent: 'WebAgent') -> bool:
        """Method responsible for performing action it self.

        It is also responsible for reporting success or failure. Differs in implementation form action to action.
        (i.e. The subclasses might and should redefine the implementation to redefine behavior.)

        :param agent: instance of WebAgent that should perform this action with
        :type agent: WebAgent

        :return: True if action succeeded, False otherwise
        :rtype: bool

        :raises BaseException: Might raise exception depending on implementation in subclass
        """
        self._logger.info(self._description)
        self._success = True
        return self._success

    def _action_failure(self, ex: BaseException = None, msg: str = None) -> None:
        """Method responsible for reporting failure and it's cause.

        Should be used in perform_self() method's implementation and nowhere else. There by it was made protected
        method.

        :param ex: instance of Exception that caused failure if any
        :type ex: BaseException
        :param msg: text message describing or explaining failure and its probable cause.
        :type msg: str

        :return: None
        :rtype: None
        """
        self._logger.info("Action '{}' FAILED.".format(self._class_name))
        if msg is not None:
            self._logger.info(msg)

        if ex is not None:
            self._logger.warning(ex)

    def add_external_failure(self, ex: Exception = None, msg: str = None):
        """Method responsible for reporting issue that prevented this action to be executed and it's cause.

        Should be used only if something external would prevent execution of this action. If in doubt, it is
        probably not the case.

        :param ex: instance of Exception that caused failure if any
        :type ex: BaseException
        :param msg: text message describing or explaining failure and its probable cause.
        :type msg: str

        :return: None
        :rtype: None
        """
        self._logger.info("Action '{}' FAILED.".format(self._class_name))
        if msg is not None:
            self._logger.info(msg)

        if ex is not None:
            self._logger.warning(ex)

        self._success = False

    def get_exception(self) -> BaseException:
        return self._ex

    def get_result(self) -> bool:
        return self._success

    def get_failure(self) -> str or None:
        if not self._success:
            return self._failure

        return None

    def expected_redirection(self) -> bool:
        """Method returns information whether or not redirection is expected to be caused by this action.

        :return: True if redirection is expected, false otherwise
        :rtype: bool
        """
        return self._redirection

    def expected_content_change(self) -> bool:
        """Method returns information whether or not content change is expected to be caused by this action.

        :return: True if content change is expected, false otherwise
        :rtype: bool
        """
        return self._change

    def delay_for_user_to_see(self) -> int:
        """Method returns number of seconds to wait after this action is completed

        :return: delay length in seconds
        :rtype: int
        """
        return self._delay_for_user

    def set_expected_redirection(self, redirection: bool) -> None:
        """Method changes information whether or not redirection is expected to be caused by this action.

        :param redirection: True if redirection is expected, false otherwise
        :type redirection: bool
        """
        self._redirection = redirection

    def set_expected_content_change(self, change: bool) -> None:
        """Method changes information whether or not content change is expected to be caused by this action.

        :param change: True if content change is expected, false otherwise
        :type change: bool
        """
        self._change = change

    def set_delay_for_users(self, delay: int) -> None:
        """Method changes information how long to delay is needed after completing this action.

        :param delay: number of second to delay
        :type delay: int
        """
        self._delay_for_user = delay

    def wait_for_frameworks(self, agent: 'WebAgent') -> None:
        """Method invokes javascript code to wait for frameworks to finish the changes on a web page.

        Method responsible for waiting for javascript frameworks to finish the changes on a web page
        caused by this action. Some of the delay might be explicit and some is asynchronous. Delay
        is than determined by javascript framework it self, depending on when injected callback was
        invoked.

        :param agent: Instance of WebAgent that should perform this action.
        :type agent: WebAgent
        """
        page = agent.get_current_page()
        page.execute_script(render_cycle, False)
        sleep(2)
        page.execute_script(angular_loaded)

    @property
    def name(self) -> str:
        """Name of this specific instance of user action - usually class name.

        :return: Name of this specific instance of user action - usually class name.
        :rtype: str
        """
        return self._class_name

    @property
    def stop_on_failure(self) -> bool:
        """Indicates if test/scenario should be stopped if this action fails.

        Default value is True but can be redefined by action or user.

        :return: delay length in seconds
        :rtype: int
        """
        return self._stop_on_failure

    # Support and experimental methods/classes, not a part of public interface
    @staticmethod
    def _get_component(page: Page, component: str, subcomponents: list or None = None) -> Component or None:
        """Method retrieves specific component from given page model by it's name

        :param page: Internal representation of specific web page. Page model with components.
        :type page: Page
        :param component: Name of the component as defined in model to be searched for.
        :type component: str
        :param subcomponents: List of component names in order as they are nested in page model.
            These names represent path to component that is supposed to contain wanted component.
        :type subcomponents: list[str] | None

        :return: Component that was found by it's name on given path or None
        :rtype: Component | None
        """
        if subcomponents is None:
            subcomponents = list()

        component = page.get_component(component)  # type: Component

        if len(subcomponents) > 0 and component is not None:
            subcomponent = component  # type: Component
            for component_name in subcomponents:
                subcomponent = subcomponent.get_subcomponent(component_name)
                if subcomponent is None:
                    break

                component = subcomponent

        return component

    @staticmethod
    def _get_element(page: Page, selector: str, value: str, component: str = Page.ROOT_COMPONENT_NAME,
                     subcomponents: list or None = None) -> Element or None:
        """Method retrieves specified web page element (DOM node) searched for as child element of specific component

        :param page: Internal representation of specific web page. Page model with components.
        :type page: Page
        :param selector: Selector type constant, attribute of webtest.common.selector.Selector
        :type selector: str
        :param value: Value of the selector
        :type value: str
        :param component: Name of the component as defined in model to be searched for.
        :type component: str
        :param subcomponents: List of component names in order as they are nested in page model.
            These names represent path to component that is supposed to contain wanted component.
        :type subcomponents: list[str] | None

        :return: Web page element (DOM node) found based on criteria given as parameters
        :rtype: Element | None
        """
        if subcomponents is None:
            subcomponents = list()

        component = UserAction._get_component(page, component, subcomponents)
        if component is None:
            return component

        node = component.get_element_node()
        return node.get_element(node, selector, value)

    @staticmethod
    def _get_link(page: Page, text: str, component: str = Page.ROOT_COMPONENT_NAME,
                  subcomponents: list or None = None) -> Element or None:
        """Method retrieves specified web page element (DOM node) representing the link with specified text.

         Similarly to _get_element() method, link is searched for as child element of specific component.
         Internally uses selenium internal workings to search for the link it self, so there is no control
         over the search it self. Sometimes this method fails to find link that actually exists and it is
         verifiable by hand.

        :param page: Internal representation of specific web page. Page model with components.
        :type page: Page
        :param text: Expected text that user would see in web page.
        :type text: str
        :param component: Name of the component as defined in model to be searched for.
        :type component: str
        :param subcomponents: List of component names in order as they are nested in page model.
            These names represent path to component that is supposed to contain wanted component.
        :type subcomponents: list[str] | None

        :return: Web page element (DOM node) found based on criteria given as parameters
        :rtype: Element | None
        """
        if subcomponents is None:
            subcomponents = list()

        component = UserAction._get_component(page, component, subcomponents)
        if component is None:
            return component

        node = component.get_element_node()
        return node.get_link_by_partial_text(text)

    @staticmethod
    def _get_link_first_visible(page: Page, text: str, component: str = Page.ROOT_COMPONENT_NAME,
                                subcomponents: list or None = None) -> Element or None:
        """Method retrieves specified web page element (DOM node) representing the link with specified text.

         Similarly to _get_element() method, link is searched for as child element of specific component.
         Works exactly like _get_link() but uses custom selector and it's value to perform the search for the
         link it self. There is more control over the search for that and usually works, but limits the search.

        :param page: Internal representation of specific web page. Page model with components.
        :type page: Page
        :param text: Expected text that user would see in web page.
        :type text: str
        :param component: Name of the component as defined in model to be searched for.
        :type component: str
        :param subcomponents: List of component names in order as they are nested in page model.
            These names represent path to component that is supposed to contain wanted component.
        :type subcomponents: list[str] | None

        :return: Web page element (DOM node) found based on criteria given as parameters
        :rtype: Element | None
        """
        if subcomponents is None:
            subcomponents = list()

        component = UserAction._get_component(page, component, subcomponents)
        if component is None:
            return component

        node = component.get_element_node()
        link_list = node.get_multiple_elements(node, Selector.XPATH, '//*/a[contains(text(), "{}")]'.format(text))
        for link in link_list:  # type: Element
            if link.visible:
                return link

        return None


class FindComponent(UserAction):
    """Specific UserAction class. Represents the search for the specific component - i.e. check if exists.

    It is not used in general, but it might be useful in specific cases and for debugging.
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
        super(FindComponent, self).__init__(kwargs)

        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> Component or None:
        page = agent.get_current_page()  # type: Page
        try:
            component = UserAction._get_component(page, self._component, self._subcomponents)
            self._logger.info("Searching for component '{}'.".format(self._component))
            return component

        except BaseException as ex:
            self._action_failure(ex)
            return None


class FindLink(UserAction):
    """Specific UserAction class. Represents the search for the specific link - i.e. check if exists.

    It is not used in general, but it might be useful in specific cases and for debugging.
    Link is searched for as a child node of specified component.
    """
    def __init__(self, link_text: str, component_name: str = Page.ROOT_COMPONENT_NAME, *args, **kwargs):
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
        super(FindLink, self).__init__(kwargs)

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

        except BaseException as ex:
            self._action_failure(ex)
            return None


class FindElement(UserAction):
    """Specific UserAction class. Represents the search for the specific DOM element - i.e. check if exists.

    It is not used in general, but it might be useful in specific cases and for debugging.
    Element is searched for as a child node of specified component.
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
        super(FindElement, self).__init__(kwargs)

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

        except BaseException as ex:
            self._action_failure(ex)
            return None
