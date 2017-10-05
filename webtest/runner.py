#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.tests.scenarios.scenario_template import scenario as example
from webtest.tests.scenarios.hawtio.address_and_queue_handling import scenario as address_and_queue

from webtest.tests.commons import Performer
from webtest.webagent import WebAgent

# main ________________________________________________________________________
def main():
    scenarios = [
        example,
        address_and_queue,
    ]

    performer = Performer()
    agent = WebAgent()

    for scenario in scenarios:
        performer.run_scenario(*scenario, agent)

if __name__ == '__main__':
    main()