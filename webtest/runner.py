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
from webtest.common.logging.logger import get_logger

# main ________________________________________________________________________
def main(args=sys.argv[1:]) -> int:
    # success of tests that will be run - indicates exit code
    success = True

    ap = ArgumentParser()
    args = ap.parse_arguments(args)

    cfg = Configurator(args["config_file"])
    cfg.set_multiple_options(args)
    # cfg.save_as("./webtest.cfg")

    # get logger but after logging was configured
    logger = get_logger("Main")

    # loader = ScenarioLoader(cfg.get_option("scenarios_path"))
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

    for scenario_name in name_list:
        scenario = loader.load_scenario(group, scenario_name)
        if scenario is not None:
            scenarios.append(scenario)
            logger.info("Scenario '{}' successfully loaded.". format(scenario_name))
            continue

        success = False
        logger.info("Scenario '{}' not found.".format(scenario_name))


    performer = Performer()
    agent = WebAgent()

    for scenario in scenarios:
        success = performer.run_scenario(*scenario, agent=agent) and success

    if not success:
        return 1

    return 0

if __name__ == '__main__':
    exit(main())