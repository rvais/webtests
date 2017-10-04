# !/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.models.hawtio.artemis_layout_two import HawtioArtemisLayoutTwoPage
from webtest.common.http import Constants
from webtest.common.selector import Selector


class HawtioSessionsPage(HawtioArtemisLayoutTwoPage):
    def __init__(self, protocol=Constants.PROTOCOL_HTTP, host="rhel7", port=8161, uri="hawtio/artemis/sessions", *args, **kw):
        super(HawtioSessionsPage, self).__init__(protocol, host, port, uri, *args, **kw)

    def _create_template(self):
        template = super(HawtioSessionsPage, self)._create_template()

        # ( name: str, selector_type: Selector.*, selector_value: str, parent: str=None, construction_exclude=False )
        addition = [
            ('name', Selector.ID, 'none', None, True), # to be removed when content is filled in
            # content table
            # TODO: fill with actual content components
        ]

        template.extend(addition)
        return template