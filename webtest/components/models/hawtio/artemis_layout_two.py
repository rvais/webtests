#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.pagemodel.page import PageModel
from webtest.common.selector import Selector
from webtest.common.http import Constants


class HawtioArtemisLayoutTwoPage(PageModel):
    def __init__(self, protocol=Constants.PROTOCOL_HTTP, host="rhel7", port=8161, uri="hawtio/artemis", *args, **kw):
        super(HawtioArtemisLayoutTwoPage, self).__init__(protocol, host, port, uri, *args, **kw)

    def _create_template(self):
        # ( name: str, selector_type: Selector.*, selector_value: str, parent: str=None, construction_exclude=False )
        template = [
            # main layout of a template
            ('body', Selector.XPATH, '/html/body'),
            ('header', Selector.ID, 'main-nav', 'body'),
            # Hawtio has confusing layout, this would be normally called 'Header'
            ('main', Selector.ID, 'main'),
            ('left-column', Selector.XPATH, '//div/div[1]', 'main'),
            ('right-column', Selector.XPATH, '//div/div[2]', 'main'),
            ('content', Selector.ID, 'properties', 'right-column'),
            ('toast', Selector.ID, 'toast-container', 'body', True),

            # main navigation
            ('header-panel', Selector.XPATH, '//div[1]/div/div[2]/ul', 'header'),
            ('main-navigation', Selector.XPATH, '//div[2]/div/ul', 'header'),

            # additional navigation
            ('navigation-tabs', Selector.XPATH, '//div/div[2]/ng-include/ul', 'right-column'),
            ('tree-menu', Selector.XPATH, '//div/div[2]/div/div', 'left-column'),
            ('expand-tree', Selector.XPATH, '//div/div[1]/div/div[2]/i[1]', 'left-column'),
            ('collapse-tree', Selector.XPATH, '//div/div[1]/div/div[2]/i[2]', 'left-column'),
            ('navigation-tabs-drop-down', Selector.XPATH, '//li[39]/a', 'navigation-tabs'),

            # filter form
            ('results-filter', Selector.XPATH, '//*[@id="properties"]/div/div[1]/div/div[1]/form', 'main'),
            ('filter-type', Selector.ID, 'filter.values.field', 'results-filter'),
            ('filter-operation', Selector.ID, 'filter.values.operation', 'results-filter'),
            ('filter-value', Selector.TAG_NAME, 'input', 'results-filter'),
            ('filter-confirm', Selector.XPATH, '//button[1]', 'results-filter'),
            ('filter-reset', Selector.XPATH, '//button[2]', 'results-filter'),


            # content table
            # Here is content empty. This is only Base template

            # modal window with attribute values
            ('modal-window', Selector.XPATH, '//html/body/div[4]', 'body', True),
            ('attr-key', Selector.XPATH, '//form/div[2]/div[2]/fieldset/div[2]/div/input', 'modal-window', True),
            ('attr-description', Selector.XPATH, '//form/div[2]/div[2]/fieldset/div[3]/div/div/textarea', 'modal-window', True),
            ('attr-type', Selector.XPATH, '//form/div[2]/div[2]/fieldset/div[4]/div/input', 'modal-window', True),
            ('attr-key', Selector.XPATH, '//form/div[2]/div[2]/fieldset/div[2]/div/input', 'modal-window', True),
        ]
        return template
