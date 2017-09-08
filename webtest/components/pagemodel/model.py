#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.common.http import Constants as HTTP_CONST
from webtest.components.pagemodel.component import Component
from webtest.common.logger import get_logger

class PageModel(dict):

    def __init__(self, protocol: str=HTTP_CONST.PROTOCOL_HTTP, host: str="localhost", port: int=0, url: str="/", *arg, **kw):
        super(PageModel, self).__init__(*arg, **kw)

        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._protocol = protocol
        self._host = host
        self._port = port
        self._url = url

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

        return

    def _create_template(self):
        return list()

    @property
    def name(self):
        return self.__class__.name

    @property
    def url(self):
        if len(self._url) > 0 and self._url[0] == '/':
            self._url = self._url[1:]

        if self._port <= 0:
            url_format = '{}://{}/{}'
            url = url_format.format(self._protocol, self._host, self._url)
        else:
            url_format = '{}://{}:{}/{}'
            url = url_format.format(self._protocol, self._host, self._port, self._url)

        return url



