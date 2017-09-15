#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from selenium.webdriver.common.actions import interaction

from webtest.common.logger import get_logger
from webtest.components.pagemodel.element import Element

class Mouse(object):

    LEFT_BUTTON = MouseButton.LEFT
    RIGHT_BUTTON = MouseButton.RIGHT
    MIDDLE_BUTTON = MouseButton.MIDDLE

    def __init__(self, webdriver: WebDriver):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

        self._driver = webdriver
        self._device = PointerInput(interaction.POINTER, "mouse")
        self._performer = PointerActions(self._device)
        self._hold = list()

    def button_down(self, button=MouseButton.LEFT):
        self._performer.pointer_down(button)
        self._execute()

    def button_up(self, button=MouseButton.LEFT):
        self._performer.pointer_up(button)
        self._execute()

    def move_above_element(self, element: Element, x: int or None=None, y: int or None=None):
        self._performer.move_to(element.get_inner_node(), x, y)
        self._execute()

    def move_by(self, x: int or None=None, y: int or None=None):
        self._performer.move_by(x, y)
        self._execute()

    def move_to(self, x: int=0, y: int=0):
        self._performer.move_to_location(x, y)
        self._execute()

    def click(self, button=LEFT_BUTTON):
        self._performer.pointer_down(button)
        self._performer.pointer_up(button)
        self._execute()

    def press_and_hold(self, button=LEFT_BUTTON):
        self._hold.append(button)
        self._performer.pointer_down(button)
        self._execute()

    def release(self):
        for button in self._hold:
            self._performer.pointer_up(button)
        self._hold = list()
        self._execute()


    def double_click(self, button=LEFT_BUTTON):
        self._performer.pointer_down(button)
        self._performer.pointer_up(button)
        self._performer.pointer_down(button)
        self._performer.pointer_up(button)
        self._execute()

    def _execute(self):
        enc = {"actions": []}
        encoded = self._device.encode()
        if encoded['actions']:
            enc["actions"].append(encoded)

        self._driver.execute(Command.W3C_ACTIONS, enc)