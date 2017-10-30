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

#
# UserAction class represents abstraction of each possible action that user
# Can perform and by doing so interact with webpage in his browser. Class
# contains implementation of methods that are common for every action form
# test's and background code's point of view. Also has support methods for
# its subclasses. To create new user action this class needs to be subclassed,
# methods __init__() and perform_self() overridden.
#
class UserAction(object):
    #
    # Constructor. Method is responsible for initializing common attributes
    # shared by all user actions.
    #
    # @param redirection: boolean indicating if action is expected to cause redirection
    # @param page_change: boolean indicating if action is expected to cause changes
    #             on current page but page won't be redirected
    # @param delay: number of seconds to wait after this action is completed. Some actions
    #             in selenium might be done quicker that they take effect in browser or
    #             it is desired for user to se the effect of that action.
    #
    def __init__(self, redirection: bool=False, page_change: bool=False, delay: int=0, stop_on_failure: bool=True):
        self._class_name = str(self.__class__.__name__)
        self._logger = get_logger(self._class_name) # type: logging.Logger

        self._redirection = redirection
        self._change = page_change
        self._delay_for_user = delay
        self._stop_on_failure = stop_on_failure


    #
    # Method responsible for performing action it self and reporting success
    # or failure. Differs in implementation form action to action.
    #
    # @param agent: instance of WebAgent that should perform this action
    # @return True if action succeeded, False otherwise
    #
    # throw: might raise exception
    #
    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Performing generic user action.")
        return True

    #
    # Method responsible for reporting failure and it's cause.
    # Should be used in perform_self() method's implementation.
    #
    # @param ex: instance of Exception that caused failure if any
    # @param msg: text message describing or explaining failure and its
    #           probable cause.
    # @return None
    #
    def action_failure(self, ex: Exception=None, msg: str=None ):
        self._logger.info("Action '{}' FAILED.".format(self._class_name))
        if msg is not None:
            self._logger.info(msg)

        if ex is not None:
            self._logger.warning(ex)

    #
    # Method returns information whether or not redirection is expected
    # to be caused by this action.
    #
    # @param None
    # @return True if redirection is expected, false otherwise
    #
    def expected_redirection(self) -> bool:
        return self._redirection

    #
    # Method returns information whether or not content change is expected
    # to be caused by this action.
    #
    # @param None
    # @return True if content change is expected, false otherwise
    #
    def expected_content_change(self) -> bool:
        return self._change

    #
    # Method returns number of seconds to wait after this action is completed
    #
    # @param None
    # @return delay length in seconds
    #
    def delay_for_user_to_see(self) -> int:
        return self._delay_for_user

    #
    # Method changes information whether or not redirection is expected
    # to be caused by this action.
    #
    # @param True if redirection is expected, false otherwise
    # @return None
    #
    def set_expected_redirection(self, redirection: bool):
        self._redirection = redirection

    #
    # Method changes information whether or not content change is expected
    # to be caused by this action.
    #
    # @param True if content change is expected, false otherwise
    # @return None
    #
    def set_expected_content_change(self, change: bool):
        self._change = change

    #
    # Method changes information how long to delay after completing this action.
    #
    # @param int number of second to delay
    # @return None
    #
    def set_delay_for_users(self, delay: int):
        self._delay_for_user = delay

    #
    # Method responsible for waiting for javascript frameworks to finish the
    # changes on a web page caused by this action.
    #
    # @param agent: instance of WebAgent that should perform this action
    # @return None
    #
    def wait_for_frameworks(self, agent: 'WebAgent') -> None:
        page = agent.get_current_page()
        page.execute_script(render_cycle, False)
        sleep(2)
        page.execute_script(angular_loaded)


    #
    # Name of the Action, class name by default
    #
    @property
    def name(self) -> str:
        return self._class_name

    #
    # Indicates if test/scenario should be stopped if this action fails.
    # Default value is True but can be redefined by action or user.
    #
    @property
    def stop_on_failure(self) -> bool:
        return self._stop_on_failure

# Support and experimental methods/classes, not a part of public interface
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
        return node.get_element(node, selector, value)

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


    @staticmethod
    def _get_link_first_visible(
            page: Page,
            text: str,
            component: str=Page.ROOT_COMPONENT_NAME,
            subcomponents: list=list()
    ) -> Element or None:
        component = UserAction._get_component(page, component, subcomponents)
        if component is None:
            return component

        node = component.get_element_node()
        link_list = node.get_multiple_elements(node, Selector.XPATH, '//*/a[contains(text(), "{}")]'.format(text))
        for link in link_list: # type: Element
            if link.visible:
                return link

        return None


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

        except BaseException as ex:
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

        except BaseException as ex:
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

        except BaseException as ex:
            self.action_failure(ex)
            return None

# piece of code form debugging _get_link method, remove it is no longer needed
#        link_list = node.get_elements_by_tag_name("a")

#        found = None
#        logger = get_logger()
#        for link in link_list: # type: Element
#            logger.info("link")
#            try:
#                link.text.index(text)
#                found = link
#            except ValueError:
#                pass
#
#        return found
#