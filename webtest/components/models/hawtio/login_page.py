#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.page import PageModel
from webtest.common.selector import Selector
from webtest.common.http import Constants


class HawtioLoginPageNS(PageModel):
    def __init__(self,protocol=Constants.PROTOCOL_HTTP, host="rhel7", port=8161, uri="hawtio", *arg, **kw):
        super(HawtioLoginPageNS, self).__init__(protocol, host, port, uri, *arg, **kw)

    def _create_template(self):
        # ( name: str, selector_type: Selector.*, selector_value: str, parent: str=None)
        template = [
            ('body', Selector.XPATH, '/html/body'),
            ('main', Selector.ID, 'main'),
            ('login-form', Selector.XPATH, '//div/div/div[2]/div/div/div/form', 'main'),
            ('user-name', Selector.XPATH, '//fieldset/div[2]/div/input', 'login-form'),
            ('user-password', Selector.XPATH, '//fieldset/div[3]/div/input', 'login-form'),
            ('remember-checkbox', Selector.XPATH, '//fieldset/div[4]/div/label/input', 'login-form'),
            ('send-button', Selector.XPATH, '//fieldset/div[4]/div/button', 'login-form'),
        ]
        return template