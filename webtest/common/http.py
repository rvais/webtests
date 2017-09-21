#!/usr/bin/env python3
#
# Framework for testing web applications - proof of concept
# Authors:  Roman Vais <rvais@redhat.com>
#

import urllib.parse as urlparse

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

class URL(object):
    def __init__(
            self,
            scheme: str=Constants.PROTOCOL_HTTP,
            host: str="localhost",
            port: int=0,
            uri: str="/",
            query: str='',
            fragment: str=''
    ):

        if len(uri) > 0 and uri[0] == '/':
            uri = uri[1:]

        self._scheme = scheme
        self._host_name = host
        self._port = port
        self._uri = uri
        self._query_string = query
        self._query = urlparse.parse_qs(query) #, strict_parsing=True)
        self._fragment = fragment

    def __eq__(self, other: 'URL'):
        similar = self.is_similar_to(other)
        try:
            if similar:
                similar = similar and self._fragment == other.fragment
                similar = similar and self._query_string == other.query_string
        except Exception:
            similar = False

        return similar

    @staticmethod
    def parse(url: str) -> 'URL' or None:
        scheme, net_location, uri, query, fragment = urlparse.urlsplit(url) # type:str

        net_location = net_location.split(':')
        if len(net_location) > 2:
            raise ValueError("Error while parsing net-location.")
        elif len(net_location) < 2:
            net_location.append(0)

        host, port = tuple(net_location)
        port = int(port)

        return URL(scheme, host, port, uri, query, fragment)


    def string(self, with_query: bool=False, with_fragment: bool=False) -> str:

        if self._port <= 0:
            url_format = '{}://{}/{}'
            full_url = url_format.format(self._scheme, self._host_name, self._uri)
        else:
            url_format = '{}://{}:{}/{}'
            full_url = url_format.format(self._scheme, self._host_name, self._port, self._uri)

        if  with_query:
            full_url += "?" + self._query_string

        if  with_fragment:
            full_url += "#" + self._fragment

        return full_url

    def __str__(self):
        return self.string()

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def host_name(self) -> str:
        return self._host_name

    @property
    def port(self) -> int:
        return self._port

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def query_string(self) -> str:
        return self._query_string

    @property
    def fragment(self) -> str:
        return self._fragment

    def is_in_query(self, variable: str, value: str or None=None) -> bool:
        present = variable in self._query.keys()
        if value is not None:
            present = present and value == self._query[variable]
        return present

    def is_similar_to(self, other: 'URL') -> bool:
        similar = True
        if not isinstance(other, URL):
            return False

        similar = similar and self._scheme == other.scheme
        similar = similar and self._host_name == other.host_name
        similar = similar and self._port == other.port
        similar = similar and self._uri == other.uri

        return similar















