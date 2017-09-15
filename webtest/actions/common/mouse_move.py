#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.actions.mouse_action import MouseAction
from webtest.webagent import WebAgent
from selenium.webdriver import ActionChains

class MouseMove(MouseAction):
    def __init__(self, x: int=0, y: int=0):
        super(MouseMove, self).__init__()

        self._x = x
        self._y = y



class MouseMoveByOffset(MouseMove):
    def __init__(self, x: int=0, y: int=0):
        super(MouseMoveByOffset, self).__init__(x,y)

    def perform_self(self, agent: 'WebAgent'):
        self._logger.info("Performing mouse move to with offset x:{x} ; y:{y}.".format(x=self._x, y=self._y))
        try:
            mouse = agent.get_mouse()
            mouse.move_by(self._x, self._y)
            return True

        except Exception as ex:
            self.action_failure(ex)
            return False

class MouseMoveTo(MouseMove):
    def __init__(self, x: int=0, y: int=0):
        super(MouseMoveTo, self).__init__(x,y)

    def perform_self(self, agent: 'WebAgent'):
        self._logger.info("Performing mouse move to position x:{x} ; y:{y}.".format(x=self._x, y=self._y))
        try:
            mouse = agent.get_mouse()
            mouse.move_to(self._x, self._y)
            return True

        except Exception as ex:
            self.action_failure(ex)
            return False
