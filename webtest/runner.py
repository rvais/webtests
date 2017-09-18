#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

from webtest.webagent import WebAgent
from webtest.common.selector import Selector
from webtest.actions.common.open_browser import OpenBrowser
from webtest.actions.common.visit_page import VisitPageByName
from webtest.actions.common.close_browser import CloseBrowser
from webtest.actions.common.click import ClickOnComponent, ClickOnLink, ClickOnElement
from webtest.actions.common.fill_form import FillForm
from webtest.components.models.hawtio.login_page import HawtioLoginPageNS
from webtest.components.models.hawtio.attributes_page import HawtioArtemisPage
from webtest.tests.commons import Performer

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

    steps = [
        OpenBrowser(),
        VisitPageByName("HawtioLoginPageNS"),
        FillForm(login, 'main', 'login-form'),
        ClickOnComponent('main', 'login-form', 'send-button', redirection=True),
        ClickOnComponent('main', 'left-column', 'expand-tree'),
        ClickOnComponent('main', 'left-column', 'collapse-tree'),
        ClickOnLink('admin', 'body', 'header', 'header-panel', redirection=False, page_change=False),
        ClickOnLink("Log out", 'body', 'header', 'header-panel', redirection=False, page_change=True),
        ClickOnElement(Selector.XPATH, '//*/input[@value="Yes"]', 'body', 'modal-window', delay=5),
        CloseBrowser()
    ]

    performer = Performer()
    performer.perform_actions(agent, steps)




if __name__ == '__main__':
    main()