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

#
# PageModel class represents knowledge about the web page that user has
# available. Namely it is a templates of the website and URL address by
# which to access it. Class contains implementation of methods that are
# used for interaction with the template, but actual template is empty.
# To create new template this page should be subclassed and method
# _create_template() overridden.
#
class PageModel(dict):
    #
    # Constructor. Method requires URL information so page can be paired with template.
    # Multiple pages with different URLs to access can share the same template but not
    # the same instance of template. (Can be improved upon in the future)
    #
    # @param host: hostname that is part of URL (e.g. www.example.com or IP address)
    # @param port: port number in case it is not standard port 80
    #              value 0 means not uo use port number in URL
    # @param uri: string that is usually part of HTTP GET request
    # @param protocol: in some cases called schema - "http" or "https"
    #
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

    #
    # Method is supposed to return list of tuples, that are representing page components.
    # @param None
    # @return list of tuples representing template of page
    #
    def _create_template(self):
        return list()

    #
    # Template's name. Class name by default.
    #
    @property
    def name(self):
        return self._name

    #
    # String representing URL that you can see in address bar in the browser.
    #
    @property
    def url_complete(self) -> str:
        return self._url.format()

    #
    # String representing URL that you can see in address bar in the browser
    # without query part. (what follows after '?' or '#' characters)
    #
    @property
    def url_short(self) -> str:
        return self._url.format()

    #
    # Object representing URL, instance of URL class.
    #
    @property
    def url(self):
        return self._url


    #
    # Method returns list of individual parts of web page as they are defined
    # in template - their Component class instance representation.
    # @param None
    # @return list of Component instances or empty list
    #
    def get_component_list(self):
        return copy(self._component_list)

    #
    # Method creates duplicate of this Page model with different name and possibly
    # with different URL location.
    #
    # @param host: hostname that is part of URL (e.g. www.example.com or IP address)
    # @param port: port number in case it is not standard port 80
    #              value 0 means not uo use port number in URL
    # @param uri: string that is usually part of HTTP GET request
    # @param protocol: in some cases called schema - "http" or "https"
    # @return instance of PageModel, with duplicate of this one's template
    #
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