#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent

class CloseBrowser(UserAction):

    def __init__(self):
        super(CloseBrowser, self).__init__()

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Closing browser.")
        agent.close_browser()
        return True

    def delay_for_user_to_see(self) -> bool:
        return False