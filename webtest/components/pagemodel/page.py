#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from time import sleep

from webtest.browsers.browser import Browser
from webtest.components.pagemodel.model import PageModel
from webtest.components.pagemodel.element import Element
from webtest.components.pagemodel.component import Component, RootComponent
from webtest.components.pagemodel.mock_element import MockElement
from webtest.common.logger import get_logger

class Page(object):

    ROOT_XPATH = '/html'
    ROOT_COMPONENT_NAME = 'root_element'

    def __init__(self, browser: 'Browser', model: PageModel=None):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)
        self._root = None
        self._root_component = None

        self._logger.info("Creating new instance of Page.")

        if browser is not None :
            self._browser = browser
            self._logger.info("Browser '{}' is available.".format(browser.name))

        else:
            self._browser = None
            self._logger.warning("No browser available. May cause problems in following code.")

        if model is None: # or model.url != browser.current_url:
            self._logger.warning("No page model available. May cause problems in following code.")
            model = PageModel()

        else:
            self._logger.info("Page model supplied.")

        self._model = model

    def __before_returning_element(self, getter):
        pass

    def get_root(self) -> Element or MockElement:

        if self._browser is None and self._root is None:
            self._root = MockElement()

        elif self._root is None:
            raw_root = self._browser.driver.find_element_by_xpath(Page.ROOT_XPATH)  # :Element

            self._logger.debug("Root element found is <{}> and will be set as "
                               "root element.".format(raw_root.tag_name))
            self._root = Element(raw_root)

        self.__before_returning_element(self._root)
        return self._root

    def get_component(
            self,
            component_name: str=ROOT_COMPONENT_NAME,
            subcomponent_name: str or None=None,
            search_depth: int=0
    ) -> Component or None:
        self._logger.debug("Attempt ot get component '{}'.".format(component_name))

        if component_name == Page.ROOT_COMPONENT_NAME:
            self._logger.debug("Returning root node component.")
            if self._root_component is None:
                self._root_component = RootComponent(self.get_root())
            return self._root_component

        if component_name not in self._model.keys():
            self._logger.debug("Component not found between main page components.")
            c = None # type: Component
            if search_depth:
                self._logger.debug("Searching given name in subcomponents "
                                   "with recursive depth={}.".format(search_depth))

                for name, component in self._model.items():
                    self._logger.debug("Searching in main component '{}'.".format(name))
                    c = component.get_subcomponent(component_name, search_depth > 1, search_depth) # type: Component
                    if c is not None:
                        self._logger.debug("Component '{}' found under '{}'.".format(c.name, name))
                        break

        else:
            c = self._model[component_name] # type: Component

        if (isinstance(c.get_element_node(), MockElement)
                and not isinstance(self.get_root(), MockElement)):
            self._logger.trace("Setting root <{}> for component '{}'.".format(self.get_root(), component_name))
            c.set_root(self.get_root())

        if c is not None and subcomponent_name is not None and len(subcomponent_name) > 0:
            self._logger.debug("Searching for subcomponent '{}' "
                               "under component '{}'.".format(subcomponent_name, c.name))
            c = c.get_subcomponent(component_name, search_depth > 1, search_depth)  # type: Component
            if c is not None:
                self._logger.debug("Subcomponent '{}' found.".format(c.name))
            else:
                self._logger.debug("Subcomponent '{}' was not found.".format(c.name))

        return c

    @property
    def url(self):
        if self._browser is not None:
            return self._browser.current_url

        else:
            return self._model.url





































