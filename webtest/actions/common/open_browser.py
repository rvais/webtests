#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent

class OpenBrowser(UserAction):

    def __init__(self, browser_name: str='', *args, **kwargs):
        super(OpenBrowser, self).__init__(*args, **kwargs)
        self._browser_name = browser_name

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Opening browser.")
        if len(self._browser_name) > 0:
            agent.start_up_browser(self._browser_name)
        else:
            agent.start_up_browser()
        return True
