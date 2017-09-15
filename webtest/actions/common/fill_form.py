#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent
from webtest.components.pagemodel.page import Page
from webtest.components.pagemodel.element import Element

class FillForm(UserAction):
    def __init__(self, data: dict, component_name: str=Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(FillForm, self).__init__(**kwargs)

        self._data_dictionary = data
        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> bool:
        page = agent.get_current_page()  # type: Page
        try:
            component = UserAction._get_component(page, self._component, self._subcomponents)
            self._logger.info("Filling form (component '{}').".format(component.name))
            return component.fill(self._data_dictionary)

        except Exception as ex:
            self.action_failure(ex)
            return False



class FillSpecificInputField(UserAction):
    def __init__(self, input_type: str, value: str, component_name: str = Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(FillSpecificInputField, self).__init__(**kwargs)

        self._input_type = input_type
        self._value = value
        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> bool:
            page = agent.get_current_page()  # type: Page
            try:
                self._logger.info("Filling input type='{}' with value '{}' .".format(self._input_type, self._value))
                component = UserAction._get_component(page, self._component, self._subcomponents)
                node = component.get_element_node() # type: Element
                if node.tag_name != 'input':
                    nodes = node.get_all_descendants('input', filters=['@type={}'.format(self._input_type),])
                    return nodes[0].fill_input([self._input_type, self._value, None])

            except Exception as ex:
                self.action_failure(ex)
                return False