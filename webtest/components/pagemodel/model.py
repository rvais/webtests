#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from copy import copy
from webtest.common.http import Constants as HTTP_CONST
from webtest.common.http import URL
from webtest.components.pagemodel.component import Component
from webtest.common.logger import get_logger

class PageModel(dict):

    def __init__(self, protocol: str=HTTP_CONST.PROTOCOL_HTTP, host: str="localhost", port: int=0, uri: str="/", *arg, **kwargs):
        super(PageModel, self).__init__(*arg, **kwargs)

        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._name = class_name

        self._url = URL(protocol, host, port, uri)
        self._component_list = list()

        self._logger.info("Creating '{}' page model with '{}' url address.".format(class_name, self.url))

        template = self._create_template()
        self.__fill_model(template)

    def __fill_model(self, template: list):
        if len(template) <= 0:
            self._logger.debug("No components set for this template.")
            return

        subcomponents = dict()

        self._logger.info("Filling inner dictionary with components.")
        for arg_tuple in template:
            c = Component(*arg_tuple)

            if c.parent is not None and c.parent in self.keys():
                self._logger.info("Component '{}' added to '{}' as subcomponent."
                                   .format(c.name, c.parent))
                self[c.parent].add_subcomponent(c)
                subcomponents[c.name] = c
            elif c.parent is not None and c.parent in subcomponents.keys():
                self._logger.info("Component '{}' added to '{}' as subcomponent."
                                   .format(c.name, c.parent))
                subcomponents[c.parent].add_subcomponent(c)
                subcomponents[c.name] = c
            else:
                if c.parent is not None:
                    self._logger.warning("Component '{}' added to template before its "
                                       "parent component '{}'.".format(c.name, c.parent))
                self._logger.info("Component '{}' added to inner dictionary "
                                   "as page main component.".format(c.name))
                self[c.name] = c

            if c.parent is None or (c.parent is not None and c.construct):
                pair = (c.name, c.parent)
                self._component_list.append(pair)

        return

    def __set_name(self, name: str):
        self._name = name

    def _create_template(self):
        return list()

    @property
    def name(self):
        return self._name

    @property
    def url_complete(self) -> str:
        return self._url.format()

    @property
    def url_short(self) -> str:
        return self._url.format()

    @property
    def url(self):
        return self._url

    def get_component_list(self):
        return copy(self._component_list)

    def derive_template(
            self,
            name: str,
            template: list=list(),
            scheme: str or None=None,
            host: str or None=None,
            port: int or None=None,
            uri: str or None=None,
    ) -> 'PageModel':
        scheme = scheme if scheme is not None else self._url.scheme
        host = host if host is not None else self._url.host_name
        port = port if port is not None else self._url.port
        uri = uri if uri is not None else self._url.uri
        new_model = PageModel(scheme, host, port, uri)

        new_model.__set_name(name)
        new_template = self._create_template()
        new_template.extend(template)

        new_model.__fill_model(new_template)

        return new_model