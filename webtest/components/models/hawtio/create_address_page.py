#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.models.hawtio.artemis_layout_one import HawtioArtemisLayoutOnePage
from webtest.common.selector import Selector
from webtest.common.http import Constants


class HawtioCreateAddressPage(HawtioArtemisLayoutOnePage):
    def __init__(self, protocol=Constants.PROTOCOL_HTTP, host="rhel7", port=8161, uri="console/artemis/createAddress", *args, **kw):
        super(HawtioCreateAddressPage, self).__init__(protocol, host, port, uri, *args, **kw)

    def _create_template(self):
        template = super(HawtioCreateAddressPage, self)._create_template()
        # ( name: str, selector_type: Selector.*, selector_value: str, parent: str=None, construction_exclude=False )
        addition = [
            # content of right column
            ('form', Selector.XPATH, '//*/form', 'right-column'),
            ('address-name', Selector.ID, 'addressName', 'form'),
            ('routing-type', Selector.ID, 'routingType', 'form'),
            ('submit', Selector.XPATH, '//*/button[@type="submit"]', 'form'),
        ]

        template.extend(addition)
        return template
