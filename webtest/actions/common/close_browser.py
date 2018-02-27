#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent

class CloseBrowser(UserAction):
    """Specific UserAction class. Action closes active instance of browser."""
    def __init__(self, *args, **kwargs):
        """Constructor. Method is responsible for initializing common attributes shared by all user actions.

        :param description: Documentation string of this specific instance user action. (Test documentation)
        :type description: str
        :param expected_result: Documentation string of expected outcome / consequences of this specific instance
            of user action. (Test documentation)
        :type expected_result: str
        :param redirection: Indicates whether or not should be page redirected as a consequence of this action
        :type redirection: bool
        :param page_change: Indicates whether or not should page change its content as a consequence of this action
        :type page_change: bool
        :param delay: Explicit delay, before next action may start its execution. Default is 0
        :type delay: int
        :param stop_on_failure: Indicates whether or not will scenario execution stop if action fail. Default True
        :type stop_on_failure: bool
        """
        super(CloseBrowser, self).__init__(*args, **kwargs)

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Closing browser.")
        agent.close_browser()
        return True
