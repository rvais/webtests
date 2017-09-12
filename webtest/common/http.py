#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

class Constants(object):
    PROTOCOL_HTTP = "http"
    PROTOCOL_HTTPS = "https"

def format_url(protocol: str=Constants.PROTOCOL_HTTP, host: str='localhost', port: int=0, url:str='/'):
    if len(url) > 0 and url[0] == '/':
        url = url[1:]

    if port <= 0:
        url_format = '{}://{}/{}'
        full_url = url_format.format(protocol, host, url)
    else:
        url_format = '{}://{}:{}/{}'
        full_url = url_format.format(protocol, host, port, url)

    return full_url

def relax_url(full_url: str, relax_anchor: bool=True, relax_get_method: bool=True):
    if relax_anchor:
        index = full_url.rindex('#')
        if index >= 0:
            full_url = full_url[0 : index]
    if relax_get_method:
        index = full_url.rindex('?')
        if index >= 0:
            full_url = full_url[0 : index]

    return full_url