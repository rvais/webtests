#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from time import sleep

import pytest
from webtest.webagent import WebAgent
from webtest.common.logger import get_logger
from webtest.actions.common.open_browser import OpenBrowser
from webtest.actions.common.close_browser import CloseBrowser
from webtest.actions.user_action import UserAction

@pytest.fixture(scope="module")
def page_to_test(request):
    logger = get_logger("Fixture")

    logger.info("Setup phase.")

    logger.debug("Instantiating WebAgent class.")
    agent = WebAgent()

    logger.debug("Getting browser name form the test case.")
    browser_name = getattr(request.module, "browser_name", WebAgent.BROWSER_CHROME)

    logger.debug("Starting up selected browser '{}'.".format(browser_name))
    agent.start_up_browser(browser=browser_name)

    logger.debug("Getting page model from the test case.")
    model = getattr(request.module, "page_model", None)
    if model is None:
        logger.debug("No model found. Falling back to URL settings")
        l = list()
        for attribute in ["host_name", "port", "url", "protocol"]:
            value = getattr(request.module, attribute, None)
            if value is None and attribute != "host_name":
                continue
            elif value is None and attribute == "host_name":
                raise Exception("Neither page model or url has not been provided")

            l.append(value)

        url = tuple(l)
        page = agent.go_to_page(*url)

    else:
        page = agent.get_page(page_model=model)

    sleep(2)

#    return page
    yield page

    sleep(5)

    logger.info("Tear-down phase.")
    agent.close_browser()

@pytest.fixture(scope="module")
def user_agent(request):
    logger = get_logger("Fixture")

    logger.info("Setup phase.")

    logger.debug("Getting browser name form the test case.")
    browser_name = getattr(request.module, "browser_name", WebAgent.BROWSER_CHROME)

    models = getattr(request.module, "models", list())

    logger.debug("Instantiating WebAgent class.")
    agent = WebAgent(models)

    assert agent.perform_action(OpenBrowser(browser_name))
    yield agent
    logger.info("Tear-down phase.")
    assert agent.perform_action(CloseBrowser())


class Performer(object):
    def __init__(self):
        class_name = str(self.__class__.__name__)
        self._logger = get_logger(class_name)

    def run_scenario(self, scenario_name: str="Unknown scenario", models_used: list=list(), steps: list=list(), agent: WebAgent=None) -> bool:
        if agent is None:
            self._logger.info("No WebAgent instance has been supplied -> creating new one.")
            agent = WebAgent()

        self._logger.info("Starting scenario '{}'.".format(scenario_name))
        agent.refresh_templates(models_used)
        passed = self.perform_actions(agent, steps)
        success =  passed == len(steps)

        if not success:
            self._logger.warning("Scenario '{}' FAILED with only {}/{} successful steps.".format(scenario_name, passed, len(steps)))
            return

        self._logger.warning("Scenario '{}' PASSED with {}/{} successful steps.".format(scenario_name, passed, len(steps)))
        return


    def perform_actions(self, agent: WebAgent, actions: list=list()) -> int:
        count = 0
        try:
            for action in actions: # type: UserAction
                assert agent.perform_action(action)
                count = count + 1
        except AssertionError as ex:
            agent.close_browser()

        return count
