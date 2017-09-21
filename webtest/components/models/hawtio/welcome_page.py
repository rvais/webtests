#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.page import PageModel
from webtest.common.selector import Selector
from webtest.common.http import Constants


class HawtioWelcomePage(PageModel):
    def __init__(self, *arg, **kw):
        super(HawtioWelcomePage, self).__init__(protocol=Constants.PROTOCOL_HTTP, host="rhel7", port=8161, uri="hawtio/welcome", *arg, **kw)

    def _create_template(self):
        # ( name: str, selector_type: Selector.*, selector_value: str, parent: str=None, construction_exclude=False )
        template = [
            # main layout of a template
            ('body', Selector.XPATH, '/html/body'),
            ('header', Selector.ID, 'main-nav', 'body'), # Hawtio has confusing layout, this would be normaly called 'Header'
            ('main', Selector.ID, 'main'),

            # main navigation
            ('header-panel', Selector.XPATH, '//div[1]/div/div[2]/ul', 'header'),
            ('main-navigation', Selector.XPATH, '//div[2]/div/ul', 'header'),

        ]
        return template