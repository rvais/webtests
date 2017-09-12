#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.webagent import WebAgent
from webtest.actions.common.open_browser import OpenBrowser
from webtest.actions.common.visit_page import VisitPageByName
from webtest.actions.common.close_browser import CloseBrowser
from webtest.actions.common.click import ClickOnComponent
from webtest.actions.common.fill_form import FillForm
from webtest.components.models.hawtio.LoginPage import HawtioLoginPageNS

# main ________________________________________________________________________
def main():
    models = [HawtioLoginPageNS(), ]
    agent = WebAgent(models)

    login = {
        'user-name': ('text', 'admin'),
        'user-password': ('password', 'admin'),
        'remember-checkbox': ('checkbox', False),
    }

    success = True
    success = success and agent.perform_action(OpenBrowser())
    success = success and agent.perform_action(VisitPageByName("HawtioLoginPageNS"))
    success = success and agent.perform_action(FillForm(login, 'main', 'login-form'))
    success = success and agent.perform_action(ClickOnComponent('main', 'login-form', 'send-button'))
    success = success and agent.perform_action(CloseBrowser())

    assert success

if __name__ == '__main__':
    main()