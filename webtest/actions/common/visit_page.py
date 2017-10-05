#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from time import sleep

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent
from webtest.common.http import format_url
from webtest.common.http import Constants as HTTP_CONST
from webtest.components.pagemodel.model import PageModel

# Group of actions dedicated to accessing web page by its identification.

class VisitPage(UserAction):
    def __init__(self, redirection: bool=True, page_change: bool=True, delay: int=0):
        super(VisitPage, self).__init__(redirection, page_change, delay)

class VisitPageByName(VisitPage):
    def __init__(self, page_name: str= '', *args, **kwargs):
        super(VisitPageByName, self).__init__(*args, **kwargs)
        self._page_name = page_name

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Accessing page by template named '{}'.".format(self._page_name))
        if not agent.is_browser_running():
            self.action_failure()

        page = agent.get_page(name=self._page_name)
        if page is not None:
            return True
        else:
            self.action_failure()
            return False



class VisitPageByUrl(VisitPage):

    def __init__(self, protocol: str=HTTP_CONST.PROTOCOL_HTTP, host: str="localhost", port: int=0, url: str="/", *args, **kwargs):
        super(VisitPageByUrl, self).__init__(*args, **kwargs)
        self._protocol = protocol
        self._host = host
        self._port = port
        self._url = url

    def perform_self(self, agent: 'WebAgent') -> bool:
        url = format_url(self._protocol, self._host, self._port, self._url)
        self._logger.info("Accessing page by url '{}'.".format(url))
        if not agent.is_browser_running():
            self.action_failure()

        page = agent.get_page(full_url=url)
        if page is not None:
            return True
        else:
            self.action_failure()
            return False



class VisitPageWithTemplate(VisitPage):

    def __init__(self, template: PageModel, *args, **kwargs):
        super(VisitPageWithTemplate, self).__init__(*args, **kwargs)
        self._model = template

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Accessing page by template named '{}'.".format(self._model.name))
        if not agent.is_browser_running():
            self.action_failure()

        page = agent.get_page(page_model=self._model)
        if page is not None:
            return True
        else:
            self.action_failure()
            return False