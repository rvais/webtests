#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

#//*[@id="hplogo"] | /html/body

from webtest.components.pagemodel.page import PageModel
from webtest.common.selector import Selector
from webtest.common.http import Constants

class GoogleMainPage(PageModel):

    def __init__(self, *arg, **kw):
        super(GoogleMainPage, self).__init__(protocol=Constants.PROTOCOL_HTTPS, host="www.google.cz", *arg, **kw)
        
    def _create_template(self):
        #( name: str, selector_type: Selector.*, selector_value: str)
        template = [
            ('body', Selector.XPATH, '/html/body'),
            ('logo', Selector.ID, 'hplogo'),
            ('text-input', Selector.XPATH, '//*[@id="gs_lc0"]/input[1]'),
            ('send-button', Selector.XPATH, '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'),
        ]
        return template

        
        
