#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from time import sleep

import pytest
from webtest.components.models.hawtio.LoginPage import HawtioLoginPageNS
from webtest.components.pagemodel.page import Page
from webtest.common.logger import get_logger

page_model = HawtioLoginPageNS()

class TestHawtioLoginNS(object):

    @pytest.mark.usefixtures("page_to_test")
    def test_one(self, page_to_test: Page):
        logger = get_logger("HawtioTest")
        logger.info("Test started ...")

        success = True
        original_url = page_to_test.url
        login = {
            'user-name' : ('text', 'admin'),
            'user-password' : ('password', 'admin'),
            'remember-checkbox': ('checkbox', False),
        }

        main_body = page_to_test.get_component('main')
        assert main_body.is_available
        logger.debug(main_body)

        form = main_body.get_subcomponent('login-form', True)  # :Component
        assert form.is_available
        logger.debug(str(form))

        success = success and form.fill(login)
        logger.debug(str(success))

        send_button = page_to_test.get_component('send-button')  # type: Component
        logger.debug(str(send_button))

        success = success and send_button.click()
        logger.debug(str(success))

        new_url = page_to_test.url

        success = success and len(new_url) > len(original_url)
        logger.debug("short url: '{}'".format(original_url))
        logger.debug("long url: '{}'".format(new_url))
        logger.debug("results: len(new_url) != len(original_url) {}, len(new_url) {},"
                     " len(original_url) {}".format(len(new_url) != len(original_url), len(new_url), len(original_url)))
        logger.debug(str(success))

        assert success
