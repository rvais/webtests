# !/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

# import page templates here:
from webtest.components.models.google.google import GoogleMainPage

# import user actions to be used as steps here:
from webtest.actions.common.open_browser import OpenBrowser
from webtest.actions.common.close_browser import CloseBrowser
from webtest.actions.user_action import UserAction

# import other things required here:  (ideally this section should be empty)



# config section (e.g. set host name and port for all templates)_______________
scenario_name="Example scenario"

# template_hostname = "rhel7"
# template_port = 8161



# templates section (i.e. create used page template instances)_________________
models = [
    GoogleMainPage()
]



# data section (e.g. login credentials)________________________________________
# login = {
#     'user-name': ('text', 'admin'),
#     'user-password': ('password', 'admin'),
#     'remember-checkbox': ('checkbox', False),
# }



# steps sections (here are defined individual scenario steps)__________________
steps = [
    # start browser
    OpenBrowser(),

    # generic user action, what ever needs to be done belongs here:
    UserAction(),

    # exit the browser
    CloseBrowser(),
]

scenario = (scenario_name, models, steps)