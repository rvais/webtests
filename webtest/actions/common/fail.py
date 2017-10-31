#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent

#
# Action that is supposed to fail every time. Used for debugging,
# experimentation and special case purposes.
#
class FailAction(UserAction):
    def __init__(self, *args, **kwargs):
        super(FailAction, self).__init__(*args, **kwargs)
        self._redirection = False
        self._change = False
        self._delay_for_user = 0

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Trying to fail and trying hard!")
        self.action_failure(msg="Successfully failed!")
        return False

class FailScenario(UserAction):
    def __init__(self,scenario_name: str="None", *args, **kwargs):
        super(FailScenario, self).__init__(*args, **kwargs)
        self._scenario_name = scenario_name
        self._redirection = False
        self._change = False
        self._delay_for_user = 0

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Scenario '{}' has no steps to perform!".format(self._scenario_name))
        self.action_failure(msg="Scenario '{}' has not been found!".format(self._scenario_name))
        return False