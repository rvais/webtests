#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent

#
# Action starts new instance of specified browser.
#
class OpenBrowser(UserAction):
    """Specific UserAction class. Action creates new instance of browser and starts it.

    Action may reuse already existing instance of browser if the name of browser is the same as of that instance.
    In that case browser is reconfigured and restarted if not running.
    """
    def __init__(self, browser_name: str='', *args, **kwargs):
        """Constructor. Method is responsible for initializing common attributes shared by all user actions.

        :param browser_name: Name of the web browser to be opened. Internal constant.
            Correct value for current session/run can be found in configurator.
        :type browser_name: str
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
        super(OpenBrowser, self).__init__(*args, **kwargs)
        self._browser_name = browser_name

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Opening browser.")
        if len(self._browser_name) > 0:
            agent.start_up_browser(self._browser_name)
        else:
            agent.start_up_browser()
        return True
