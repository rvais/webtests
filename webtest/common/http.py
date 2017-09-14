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
        try:
            index = full_url.rindex('#')
            if index >= 0:
                full_url = full_url[0 : index]
        except ValueError as ex:
            pass

    if relax_get_method:
        try:
            index = full_url.rindex('?')
            if index >= 0:
                full_url = full_url[0 : index]
        except ValueError as ex:
            pass

    return full_url

def cut_host_from_url(full_url: str) -> str:
    index = len("{}://".format(Constants.PROTOCOL_HTTPS))
    try:
        index = full_url.index("/", index)
        full_url = full_url[index:]
    except Exception as ex:
        pass

    return full_url