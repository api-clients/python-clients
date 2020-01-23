import json
import logging
import typing

import requests


class Method:
    name = '???'
    m_type = '???'
    url_ = ''
    headers = None
    body = None
    params = None
    count = 0
    auth = None
    files = typing.Dict
    """
    :arg name: name of method 
    :arg m_type: type of method (GET, POST, PUT etc...)
    :arg url_: type of method (endpoint, for example: https://localhost:5000/api-docs. In this case is api-docs)
    :arg headers: headers for request
    :arg body_: body of request
    :arg params: query params  
    :arg count: count params into path of url
    :arg auth: requests authorisation
    :arg files: list of files
    """

    def __init__(self, *args):
        assert len(args) == self.count, f'count path args must by equal count. count: {self.count}. passed: {len(args)}'
        self.__args = args

    @property
    def url(self):
        return self.url_ % self.__args

    @staticmethod
    def response_process(resp, status_code):
        return resp, status_code

    @staticmethod
    def request_process(req):
        return req

    @property
    def body_(self):
        return json.dumps(self.body)


class Client:
    def __init__(self, endpoint, proxies=None):
        """
        This client implements http-client

        :param endpoint: base url for requests
        :param proxies: dict with proxies ({'schema': 'endpoint'})
        """
        self.endpoint = endpoint
        self.proxies = proxies

    def __get_url(self, method):
        return f'{self.endpoint}{method.url}'

    def request(self, method):
        m_type = method.m_type
        auth_ = method.auth
        url = self.__get_url(method)
        if m_type == 'GET':
            assert method.body_ is None, 'For GET method body must be empty'
            if self.proxies is None:
                r = requests.get(url=url, params=method.params, headers=method.headers, auth=auth_)
            else:
                r = requests.get(url=url, params=method.params, headers=method.headers, proxies=self.proxies, auth=auth_)
        elif m_type == 'FILE':
            assert method.files is not None, 'For FILE attribute file must not be empty'
            if self.proxies is not None:
                r = requests.post(url=url, params=method.params, data=method.body_, headers=method.headers, auth=auth_,
                                  files=method.files)
            else:
                r = requests.post(url=url, params=method.params, data=method.body_, headers=method.headers,
                                  proxies=self.proxies, auth=auth_, files=method.files)
        elif m_type == 'POST':
            if self.proxies is None:
                r = requests.post(url=url, params=method.params, data=method.body_, headers=method.headers, auth=auth_)
            else:
                r = requests.post(url=url, params=method.params, data=method.body_, headers=method.headers,
                                  proxies=self.proxies, auth=auth_)
        elif m_type == 'DELETE':
            if self.proxies is None:
                r = requests.delete(url=url, params=method.params, data=method.body_, headers=method.headers, auth=auth_)
            else:
                r = requests.delete(url=url, params=method.params, data=method.body_, headers=method.headers,
                                    proxies=self.proxies, auth=auth_)
        elif m_type == 'PATCH':
            if self.proxies is None:
                r = requests.patch(url=url, params=method.params, data=method.body_, headers=method.headers, auth=auth_)
            else:
                r = requests.patch(url=url, params=method.params, data=method.body_, headers=method.headers,
                                    proxies=self.proxies, auth=auth_)
        elif m_type == 'PUT':
            if self.proxies is None:
                r = requests.put(url=url, params=method.params, data=method.body_, headers=method.headers, auth=auth_)
            else:
                r = requests.put(url=url, params=method.params, data=method.body_, headers=method.headers,
                                    proxies=self.proxies, auth=auth_)
        else:
            raise Exception("\nnot implemented method request: %s" % method.m_type)
        try:
            if r is None or len(r.content) == 0:
                return method.response_process({}, r.status_code)
            return method.response_process(r.json(), r.status_code)
        except Exception as e:
            logging.info(f'not a json response: {e}')
            return method.response_process({}, 520)
