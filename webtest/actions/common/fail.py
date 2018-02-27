#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.user_action import UserAction
from webtest.webagent import WebAgent


class FailAction(UserAction):
    """Specific UserAction class. Action that is supposed to fail every time.

    Used mainly for debugging, experimentation and occasionally for special case purposes.
    Doesn't stop execution of the whole scenario. Instead fails on its own.
    """

    def __init__(self, *args, **kwargs):
        """Constructor. Method is responsible for initializing common attributes shared by all user actions.

        Not specified params, that can be usually specified for user action, are ignored (overridden by preset values).

        :param description: Documentation string of this specific instance user action. (Test documentation)
        :type description: str
        :param expected_result: Documentation string of expected outcome / consequences of this specific instance
            of user action. (Test documentation)
        :type expected_result: str
        """
        super(FailAction, self).__init__(*args, **kwargs)
        self._redirection = False
        self._change = False
        self._delay_for_user = 0
        self._stop_on_failure = False

    def perform_self(self, agent: 'WebAgent') -> bool:
        self._logger.info("Trying to fail and trying hard!")
        self._action_failure(msg="Successfully failed!")
        return False


class FailScenario(UserAction):
    """Specific UserAction class. Action that is supposed to fail every time.

    Used mainly for debugging, experimentation and occasionally for special case purposes.
    Immediately stops execution of the whole scenario.
    """

    def __init__(self, scenario_name: str or None = None, *args, **kwargs):
        """Constructor. Method is responsible for initializing common attributes shared by all user actions.

        Not specified params, that can be usually specified for user action, are ignored (overridden by preset values).

        :param scenario_name: Name of the scenario that you are trying to fail. For logging purposes only.
        :type scenario_name: str | None
        :param description: Documentation string of this specific instance user action. (Test documentation)
        :type description: str
        :param expected_result: Documentation string of expected outcome / consequences of this specific instance
            of user action. (Test documentation)
        :type expected_result: str
        """
        super(FailScenario, self).__init__(*args, **kwargs)
        self._redirection = False
        self._change = False
        self._delay_for_user = 0
        self._stop_on_failure = True

        self._scenario_name = scenario_name

    def perform_self(self, agent: 'WebAgent') -> bool:
        msg = "Trying to fail scenario and trying hard!"
        if self._scenario_name is not None:
            msg = "Trying to fail scenario '{}' and trying hard!".format(self._scenario_name)

        self._logger.info(msg)
        self._action_failure(msg="Successfully failed!")
        return False
