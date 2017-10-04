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
from webtest.actions.common.click import ClickOnComponent, ClickOnLink, ClickOnElement, ClickOnLinkFirstVisible
from webtest.actions.common.fill_form import FillForm, FillSpecificElement
from webtest.actions.common.inspect import LinkExists
from webtest.actions.user_action import UserAction
from webtest.components.models.hawtio.login_page import HawtioLoginPageNS
from webtest.components.models.hawtio.attributes_page import HawtioArtemisPage
from webtest.components.models.hawtio.welcome_page import HawtioWelcomePage
from webtest.components.models.hawtio.create_address_page import HawtioCreateAddressPage
from webtest.tests.commons import Performer

# main ________________________________________________________________________
def main():

    login_page = HawtioLoginPageNS()
    welcome_page = HawtioWelcomePage()
    artemis_page = HawtioArtemisPage()
    create_address_page = HawtioCreateAddressPage()
    models = [
        login_page,
        login_page.derive_template(name="HawtioAlternativeLogin", uri="hawtio/login"),
        welcome_page,
        artemis_page,
        artemis_page.derive_template(name="HawtioArtemisJMXattributes", uri="hawtio/jmx/attributes"),
        create_address_page,
    ]

    agent = WebAgent(models)

    login = {
        'user-name': ('text', 'admin'),
        'user-password': ('password', 'admin'),
        'remember-checkbox': ('checkbox', False),
    }

    address = {
        'address-name': ('text', 'pokus'),
        'routing-type': ['Anycast',],
    }

    steps = [

        # login test
        OpenBrowser(),
        VisitPageByName("HawtioLoginPageNS"),
        FillForm(login, 'main', 'login-form'),
        ClickOnComponent('main', 'login-form', 'send-button', redirection=True),

        # tree expand-collapse test
        ClickOnLink('Artemis', 'body', 'header', 'main-navigation', redirection=True),
        ClickOnComponent('main', 'left-column', 'expand-tree'),
        ClickOnComponent('main', 'left-column', 'collapse-tree'),
        ClickOnComponent('main', 'left-column', 'expand-tree'),

        # create address test
        ClickOnLink('addresses', 'main', 'tree-menu', redirection=False, page_change=False),
        ClickOnComponent('main', 'right-column', 'navigation-tabs', 'navigation-tabs-drop-down', delay=5),
        UserAction(),
        ClickOnLink('Create', 'main', 'right-column', 'navigation-tabs', page_change=True),
        FillForm(address, 'main', 'right-column', 'form'),
        ClickOnComponent('main', 'right-column', 'form', 'submit'),
        ClickOnElement(Selector.XPATH, '//*/button', 'body', 'toast', delay=8), # close the bubble

        ClickOnComponent('main', 'left-column', 'collapse-tree'),
        ClickOnComponent('main', 'left-column', 'expand-tree'),

#        LinkExists(address['address-name'][1], 'main', 'left-column', 'tree-menu'),
        LinkExists(address['address-name'][1], 'main', 'left-column', 'tree-menu'),
        ClickOnLinkFirstVisible(address['address-name'][1], 'main', 'left-column', 'tree-menu', redirection=False, delay=10),


        # create queue test
#        ClickOnComponent('main', 'left-column', 'expand-tree'),
 #       ClickOnLink('addresses', 'main', 'tree-menu', redirection=False, page_change=False),
  #      ClickOnComponent('main', 'right-column', 'navigation-tabs', 'navigation-tabs-drop-down'),
   #     ClickOnLink('Create', 'main', 'right-column', 'navigation-tabs', page_change=True),
    #    FillForm(address, 'main', 'right-column', 'form'),
     #   ClickOnComponent('main', 'right-column', 'form', 'submit'),
      #  ClickOnElement(Selector.XPATH, '//*/button', 'body', 'toast', delay=8),  # close the bubble


        # logout test
        ClickOnLink('admin', 'body', 'header', 'header-panel', redirection=False, page_change=False),
        ClickOnLink("Log out", 'body', 'header', 'header-panel', redirection=False, page_change=True),
        ClickOnElement(Selector.XPATH, '//*/input[@value="Yes"]', 'body', 'modal-window', delay=5),
        CloseBrowser()
    ]

    performer = Performer()
    performer.perform_actions(agent, steps)

if __name__ == '__main__':
    main()