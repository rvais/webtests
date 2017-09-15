#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.actions.mouse_action import MouseAction
from webtest.webagent import WebAgent
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.element import Element
from webtest.components.pagemodel.component import Component

class ClickOnComponent(UserAction):
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
                self.action_failure(msg="Component is not visible.")
                return False

        except Exception as ex:
            self.action_failure()
            return False



class ClickOnLink(UserAction):
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
        if True: #try:
            link = UserAction._get_link(page, self._link_text, self._component, self._subcomponents) # type: Element
            if link.visible:
                self._logger.info("Clicking on link with text '{}'.".format(self._link_text))
                return link.click(link)
            else:
                self.action_failure(msg="Element is not visible.")
                return False

        else : #except Exception as ex:
            ex = None
            self.action_failure(ex)
            return False



class ClickOnElement(UserAction):
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
                self.action_failure(msg="Element is not visible.")
                return False

        except Exception as ex:
            self.action_failure(ex)
            return False

class MouseClick(MouseAction):
    def __init__(self):
        super(MouseClick, self).__init__()

    def perform_self(self, agent: 'WebAgent'):
        self._logger.info("Performing mouse click on current position.")
        try:
            mouse = agent.get_mouse()
            mouse.click()
            return True

        except Exception as ex:
            self.action_failure(ex)
            return False

class MouseDoubleClick(MouseAction):
    def __init__(self):
        super(MouseDoubleClick, self).__init__()

    def perform_self(self, agent: 'WebAgent'):
        self._logger.info("Performing mouse double-click on current position.")
        try:
            mouse = agent.get_mouse()
            mouse.double_click()
            return True

        except Exception as ex:
            self.action_failure(ex)
            return False