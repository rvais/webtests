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
                    return nodes[0].fill_input(node, [self._input_type, self._value, None])
                else:
                    return node.fill_input(node, [self._input_type, self._value, None])

            except Exception as ex:
                self.action_failure(ex)
                return False

class FillSpecificElement(UserAction):
    def __init__(self, tagname: str, attributes: dict=None, value: str or list or bool='',  component_name: str = Page.ROOT_COMPONENT_NAME, *args, **kwargs):
        super(FillSpecificElement, self).__init__(**kwargs)

        self._tag = tagname
        self._attributes = attributes if attributes is not None and isinstance(attributes, dict) else dict()
        self._value = value
        self._component = component_name
        self._subcomponents = list()
        if len(args) > 0:
            self._subcomponents.extend(list(args))

    def perform_self(self, agent: 'WebAgent') -> bool:
            page = agent.get_current_page()  # type: Page
            try:
                self._logger.info("Filling specified element <{}> with value '{}' .".format(self._tag, self._value))
                component = UserAction._get_component(page, self._component, self._subcomponents)
                node = component.get_element_node() # type: Element
                if node.tag_name == self._tag:
                    success = True
                    for attr in  self._attributes.keys():
                        v = node.get_attribute(node, attr)
                        if self._attributes[attr] != v:
                            self._logger.debug('<{tag} {attr}="{value}"> found vs. '
                                               '<{tag} {attr}="{rq}"> required'.format(tag=self._tag, attr=attr, value=v, rq=self._attributes[attr]))
                            success = False

                    if not success:
                        self.action_failure(msg="Element found does not have all required attributes or some of the values are different.")
                        return success

                    return node.fill(self._value)
                else:
                    attr_list = list()
                    for attr in self._attributes.keys():
                        attr_list.append('@{attr}="{value}"'.format(attr=attr, value=self._attributes[attr]))

                    if len(attr_list) > 0:
                        selector = '[{}]'.format(' and '.join(attr_list))
                    else:
                        selector = ''

                    node = node.get_element_by_xpath("//*/{}{}".format(self._tag, selector))
                    return node.fill(self._value)

            except Exception as ex:
                self.action_failure(ex)
                return False