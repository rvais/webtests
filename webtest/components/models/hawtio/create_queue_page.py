# !/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.components.models.hawtio.artemis_layout_one import HawtioArtemisLayoutOnePage
from webtest.common.http import Constants
from webtest.common.selector import Selector


class HawtioQueueCreatePage(HawtioArtemisLayoutOnePage):
    def __init__(self, protocol=Constants.PROTOCOL_HTTP, host="rhel7", port=8161, uri="/console/artemis/createQueue", *args, **kw):
        super(HawtioQueueCreatePage, self).__init__(protocol, host, port, uri, *args, **kw)

    def _create_template(self):
        template = super(HawtioQueueCreatePage, self)._create_template()

        # ( name: str, selector_type: Selector.*, selector_value: str, parent: str=None, construction_exclude=False )
        addition = [
            # content of right column
            ('form', Selector.XPATH, '//*/form', 'right-column'), # form to create queue
            ('queue-name-input', Selector.ID, 'queueName', 'form'),
            ('routing-type-select', Selector.ID, 'routingType', 'form'),
            ('durable-checkbox', Selector.ID, 'durable', 'form'),
            ('filter-input', Selector.ID, 'filter', 'form'),
            ('max-consumers-input', Selector.ID, 'maxConsumers', 'form'),
            ('purge-checkbox', Selector.ID, 'purgeWhenNoConsumers', 'form'),
            ('submit', Selector.XPATH, '//*/button[@type="submit"]', 'form')
        ]

        template.extend(addition)
        return template