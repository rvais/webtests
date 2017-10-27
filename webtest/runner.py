#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#
import sys
import os

from webtest.config.argparser import ArgumentParser
from webtest.config.scenario_loader import ScenarioLoader
from webtest.config.configurator import Configurator

from webtest.webagent import WebAgent
from webtest.tests.commons import Performer

# main ________________________________________________________________________
def main(args=sys.argv[1:]) -> int:

    ap = ArgumentParser()
    args = ap.parse_arguments(args)

    cfg = Configurator(args["config_file"])
    cfg.set_multiple_options(args)
    cfg.save_as("./webtest.cfg")

    #loader = ScenarioLoader(cfg.get_option("scenarios_path"))
    sp = cfg.get_option("scenarios_path")
    if not os.path.isabs(sp):
        sp = os.path.abspath(sp)

    loader = ScenarioLoader()
    loader.add_all_scenarios(sp)

    scenarios = list()

    group = cfg.get_option("scenarios_class")
    name_list = cfg.get_option("execute_scenarios")
    if name_list is None:
        name_list = list()

    for scenario in name_list:
        scenario = loader.load_scenario(group, scenario)
        if scenario is not None:
            scenarios.append(scenario)

    performer = Performer()
    agent = WebAgent()

    success = True
    for scenario in scenarios:
        success = success and performer.run_scenario(*scenario, agent)

    if not success:
        return 1

    return 0

if __name__ == '__main__':
    exit(main())