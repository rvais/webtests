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

