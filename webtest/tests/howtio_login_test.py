#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from time import sleep

import pytest
from webtest.components.models.hawtio.login_page import HawtioLoginPageNS
from webtest.components.pagemodel.page import Page
from webtest.common.logger import get_logger

page_model = HawtioLoginPageNS()

class NotTestHawtioLoginNS(object):

    @pytest.mark.usefixtures("page_to_test")
    def nope_test_one(self, page_to_test: Page):
        logger = get_logger("HawtioTest")
        logger.info("Test started ...")

        success = True
        original_url = page_to_test.url
        login = {
            'user-name': ('text', 'admin'),
            'user-password': ('password', 'admin'),
            'remember-checkbox': ('checkbox', False),
        }

        main_body = page_to_test.get_component('main')
        assert main_body.is_available
        logger.debug(main_body)

        form = main_body.get_subcomponent('login-form', True)  # type: Component
        assert form is not None
        logger.debug(str(form))

        success = success and form.fill(login)
        logger.debug("Form filling ... {}".format(success))
        sleep(1)

        send_button = form.get_subcomponent('send-button', True)
        logger.debug(str(send_button))

        success = success and send_button.click()  # :Component
        logger.debug("Send button click ... {}".format(success))
        sleep(1)

        new_url = page_to_test.url

        success = success and len(new_url) > len(original_url)
        logger.debug("short url: '{}'".format(original_url))
        logger.debug("long url: '{}'".format(new_url))
        logger.debug("results: len(new_url) != len(original_url) {}, len(new_url) {},"
                     " len(original_url) {}".format(len(new_url) != len(original_url), len(new_url), len(original_url)))
        logger.debug(str(success))

        assert success
