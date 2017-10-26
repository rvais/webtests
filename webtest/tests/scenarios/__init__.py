# !/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
from webtest.config.scenario_loader import ScenarioLoader

loader = ScenarioLoader()
loader.add_all_scenarios(__path__)