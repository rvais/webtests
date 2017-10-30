#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from time import sleep

import pytest
from webtest.components.models.google.google import GoogleMainPage
from webtest.components.pagemodel.page import Page
from webtest.common.logging.logger import get_logger

page_model = GoogleMainPage()


class TestGooglePage(object):

    @pytest.mark.usefixtures("page_to_test")
    def test_one(self, page_to_test: Page):
        logger = get_logger("GoogleTest")
        logger.info("Test started ...")

        success = True
        short_url = page_to_test.url
        input_data = ("text", "Messaging QE")

        text_input = page_to_test.get_component('text-input')
        logger.debug(str(text_input))

        success = success and text_input.fill(input_data) # :Component
        logger.debug(str(success))
        sleep(1)

        send_button = page_to_test.get_component('send-button')
        logger.debug(str(send_button))

        success = success and send_button.click()  # :Component
        logger.debug(str(success))
        sleep(1)

        long_url = page_to_test.url

        success = success and len(long_url) > len(short_url)
        logger.debug("short url: '{}'".format(short_url))
        logger.debug("long url: '{}'".format(long_url))
        logger.debug("results: len(long_url) > len(short_url) {}, len(long_url) {},"
                     " len(short_url) {}".format(len(long_url) > len(short_url), len(long_url), len(short_url)))
        logger.debug(str(success))

        assert success

    @pytest.mark.usefixtures("page_to_test")
    def test_two(self, page_to_test: Page):
        assert False