#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from time import sleep

import pytest
from webtest.webagent import WebAgent
from webtest.common.logger import get_logger

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
        page = agent.get_page(pmodel=model)

    sleep(2)

#    return page
    yield page

    sleep(5)

    logger.info("Tear-down phase.")
    agent.close_browser()
