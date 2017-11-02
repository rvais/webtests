# !/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

# import page templates here:
from webtest.components.models.hawtio.login_page import HawtioLoginPageNS
from webtest.components.models.hawtio.welcome_page import HawtioWelcomePage
from webtest.components.models.hawtio.attributes_page import HawtioAttributesPage
from webtest.components.models.hawtio.create_address_page import HawtioCreateAddressPage
from webtest.components.models.hawtio.create_queue_page import HawtioQueueCreatePage

# import user actions to be used as steps here:
from webtest.actions.common.open_browser import OpenBrowser
from webtest.actions.common.close_browser import CloseBrowser
from webtest.actions.common.visit_page import VisitPageByName
from webtest.actions.common.click import ClickOnComponent, ClickOnLink, ClickOnElement, ClickOnLinkFirstVisible
from webtest.actions.common.fill_form import FillForm
from webtest.actions.common.inspect import LinkExists
from webtest.actions.user_action import UserAction

# import other things required here:  (ideally this section should be empty)
from webtest.common.selector import Selector



# config section (e.g. set host name and port for all templates)_______________
scenario_name = "Address&Queue - Create"

template_hostname = "rhel7"
template_port = 8161



# templates section (i.e. create used page template instances)_________________
login_page = HawtioLoginPageNS(host=template_hostname, port=template_port)

models = [
    login_page,
    login_page.derive_template(name="HawtioAlternativeLogin", uri="hawtio/login"),
    HawtioWelcomePage(host=template_hostname, port=template_port),
    HawtioAttributesPage(host=template_hostname, port=template_port),
    HawtioCreateAddressPage(host=template_hostname, port=template_port),
    HawtioQueueCreatePage(host=template_hostname, port=template_port),
]



# data section (e.g. login credentials)________________________________________
login = {
    'user-name': ('text', 'admin'),
    'user-password': ('password', 'admin'),
    'remember-checkbox': ('checkbox', False),
}

address = {
    'address-name': ('text', 'pokus'),
    'routing-type': ['Anycast', ],
}

queue = {
    'queue-name-input': ('text', 'pokus-queue'),
    'routing-type-select': ['Anycast', ],
    'durable-checkbox': ('checkbox', True),
    'filter-input': ('text', 'filter'),
    'max-consumers-input': ('number', 20),
    'purge-checkbox': ('checkbox', False),
}


# steps sections (here are defined individual scenario steps)__________________
steps = [
    # start browser
    OpenBrowser(),

    # login to Hawtio using correct credentials from data section
    VisitPageByName("HawtioLoginPageNS"),
    FillForm(login, 'main', 'login-form'),
    ClickOnComponent('main', 'login-form', 'send-button', redirection=True),

    # tree menu manipulation (tree expand-collapse test)
    ClickOnLink('Artemis', 'body', 'header', 'main-navigation', redirection=True),
    ClickOnComponent('main', 'left-column', 'expand-tree'),
    ClickOnComponent('main', 'left-column', 'collapse-tree'),
    ClickOnComponent('main', 'left-column', 'expand-tree'),

    # create address
    ClickOnLink('addresses', 'main', 'tree-menu', redirection=False, page_change=False),
    ClickOnComponent('main', 'right-column', 'navigation-tabs', 'navigation-tabs-drop-down', delay=5),
    ClickOnLink('Create', 'main', 'right-column', 'navigation-tabs', page_change=True),
    FillForm(address, 'main', 'right-column', 'form'),
    ClickOnComponent('main', 'right-column', 'form', 'submit', page_change=True),
    ClickOnElement(Selector.XPATH, '//*/button', 'body', 'toast', delay=8), # close the "success" bubble, doesn't seem to be working

    # force tree menu to refresh
    ClickOnComponent('main', 'left-column', 'collapse-tree'),
    ClickOnComponent('main', 'left-column', 'expand-tree'),

    # check that address has been created by it's existence in tree menu
    LinkExists(address['address-name'][1], 'main', 'left-column', 'tree-menu'),

    # create queue
    ClickOnLinkFirstVisible(address['address-name'][1], 'main', 'left-column', 'tree-menu', redirection=False, delay=3),
    ClickOnLink('Attributes', 'main', 'right-column', 'navigation-tabs', page_change=True),
    ClickOnComponent('main', 'right-column', 'navigation-tabs', 'navigation-tabs-drop-down', delay=5),
    ClickOnLink('Create', 'main', 'right-column', 'navigation-tabs', page_change=True),
    FillForm(queue, 'main', 'right-column', 'form'),
    ClickOnComponent('main', 'right-column', 'form', 'submit', page_change=True),
    ClickOnElement(Selector.XPATH, '//*/button', 'body', 'toast', delay=8), # close the "success" bubble, doesn't seem to be working

    # force tree menu to refresh
    ClickOnComponent('main', 'left-column', 'collapse-tree'),
    ClickOnComponent('main', 'left-column', 'expand-tree'),

    # check that queue has been created by it's existence in tree menu
    LinkExists(queue['queue-name-input'][1], 'main', 'left-column', 'tree-menu'),
    ClickOnLinkFirstVisible(queue['queue-name-input'][1], 'main', 'left-column', 'tree-menu', redirection=False, delay=3),

    # logout from hawtio
    ClickOnLink('admin', 'body', 'header', 'header-panel', redirection=False, page_change=False),
    ClickOnLink("Log out", 'body', 'header', 'header-panel', redirection=False, page_change=True),
    ClickOnElement(Selector.XPATH, '//*/input[@value="Yes"]', 'body', 'modal-window', delay=5),

    # exit the browser
    CloseBrowser(),
]

scenario = (scenario_name, models, steps)