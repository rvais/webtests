#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.page import PageModel
from webtest.common.selector import Selector
from webtest.common.http import Constants


class HawtioArtemisPage(PageModel):
    def __init__(self, *arg, **kw):
        super(HawtioArtemisPage, self).__init__(protocol=Constants.PROTOCOL_HTTP, host="rhel7", port=8161, url="hawtio/artemis", *arg, **kw)

    def _create_template(self):
        # ( name: str, selector_type: Selector.*, selector_value: str, parent: str=None, construction_exclude=False )
        template = [
            # main layout of a template
            ('body', Selector.XPATH, '/html/body'),
            ('header', Selector.ID, 'main-nav', 'body'), # Hawtio has confusing layout, this would be normaly called 'Header'
            ('main', Selector.ID, 'main'),
            ('left-column', Selector.XPATH, '//div/div[1]', 'main'),
            ('right-column', Selector.XPATH, '//div/div[2]', 'main'),
            ('content', Selector.ID, 'properties', 'right-column'),
            ('modal-window', Selector.XPATH, '/html/body/div[4]', 'body', True),

            # main navigation
            ('header-panel', Selector.XPATH, '//div[1]/div/div[2]/ul', 'header'),
            ('main-navigation', Selector.XPATH, '//div[2]/div/ul', 'header'),

            # additional navigation
            ('navigation-tabs', Selector.XPATH, '//div/div[2]/ng-include/ul', 'right-column'),
            ('tree-menu', Selector.ID, 'tree-container', 'left-column'),
            ('expand-tree', Selector.XPATH, '//div/div[1]/div/div[2]/i[1]', 'left-column'),
            ('collapse-tree', Selector.XPATH, '//div/div[1]/div/div[2]/i[2]', 'left-column'),
            ('navigation-tabs-drop-down', Selector.XPATH, '//li[42]/a', 'navigation-tabs'),

        ]
        return template

    def get_tree_address_xpath(self) -> str:
        return ''

    def get_tree_queue_xpath(self) -> str:
        return ''

    # <a href="#" class="dynatree-title">DLQ</a>

    # dynatree-node dynatree-folder dynatree-lastsib dynatree-exp-el dynatree-expanded org-apache-activemq-artemis-addresses-folder dynatree-has-children dynatree-ico-ef
    # dynatree-node dynatree-folder dynatree-lastsib dynatree-exp-cl org-apache-activemq-artemis-"anycast" can-invoke dynatree-ico-cf dynatree-active