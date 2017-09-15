#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.webagent import WebAgent
from webtest.actions.common.open_browser import OpenBrowser
from webtest.actions.common.visit_page import VisitPageByName
from webtest.actions.common.close_browser import CloseBrowser
from webtest.actions.common.click import ClickOnComponent, ClickOnLink
from webtest.actions.common.fill_form import FillForm
from webtest.components.models.hawtio.LoginPage import HawtioLoginPageNS
from webtest.components.models.hawtio.attributes_page import HawtioArtemisPage

# main ________________________________________________________________________
def main():

    login_page = HawtioLoginPageNS()
    artemis_page = HawtioArtemisPage()
    models = [
        login_page,
        login_page.derive_template(name="HawtioAlternativeLogin", url="console/login"),
        artemis_page,
        artemis_page.derive_template(name="HawtioArtemisJMXattributes", url="console/jmx/attributes"),
    ]

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

    click = ClickOnComponent('main', 'login-form', 'send-button', redirection=True)
    success = success and agent.perform_action(click)

    click = ClickOnComponent('main', 'left-column', 'expand-tree')
    success = success and agent.perform_action(click)

    click = ClickOnComponent('main', 'left-column', 'collapse-tree')
    success = success and agent.perform_action(click)

    click = ClickOnLink('admin', 'body', 'header', 'header-panel', redirection=False, page_change=False)
    success = success and agent.perform_action(click)

    click = ClickOnLink("Log out", 'body', 'header', 'header-panel')#, redirection=False, page_change=False)
    success = success and agent.perform_action(click)
    success = success and agent.perform_action(CloseBrowser())

    assert success

if __name__ == '__main__':
    main()