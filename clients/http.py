import logging

import requests


class Method:
    name = '???'
    type_ = '???'
    _url = ''
    headers = None
    body = None
    params = None
    count = 0
    auth = None
    """
    :arg name: name of method 
    :arg type_: type of method (GET, POST, PUT etc...)
    :arg url: type of method (endpoint, for example: https://localhost:5000/api-docs. In this case is api-docs)
    :arg headers: headers for request
    :arg data: body of request
    :arg params: query params  
    :arg count: count params into path of url
    :arg auth: requests authorisation
    """

    def __init__(self, *args):
        assert len(args) == self.count, f'count path args must by equal count. count: {self.count}. passed: {len(args)}'
        self.__args = args

    @property
    def url(self):
        return self._url % self.__args

    @staticmethod
    def response_process(resp):
        return {}

    @staticmethod
    def request_process(req):
        return req


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
            assert method.body is None, 'For GET method body must be empty'
            if self.proxies is None:
                r = requests.get(url=url, params=method.params, headers=method.headers, auth=auth_)
            else:
                r = requests.get(url=url, params=method.params, headers=method.headers, proxies=self.proxies, auth=auth_)
        elif m_type == 'POST':
            if self.proxies is None:
                r = requests.post(url=url, params=method.params, data=method.body, headers=method.headers, auth=auth_)
            else:
                r = requests.post(url=url, params=method.params, data=method.body, headers=method.headers,
                                  proxies=self.proxies, auth=auth_)
        elif m_type == 'DELETE':
            if self.proxies is None:
                r = requests.delete(url=url, params=method.params, data=method.body, headers=method.headers, auth=auth_)
            else:
                r = requests.delete(url=url, params=method.params, data=method.body, headers=method.headers,
                                    proxies=self.proxies, auth=auth_)
        elif m_type == 'PATCH':
            if self.proxies is None:
                r = requests.patch(url=url, params=method.params, data=method.body, headers=method.headers, auth=auth_)
            else:
                r = requests.delete(url=url, params=method.params, data=method.body, headers=method.headers,
                                    proxies=self.proxies, auth=auth_)
        else:
            raise Exception("\nnot implemented method request: %s" % method.m_type)
        if r.status_code // 100 != 2:
            logging.error(f'status code: {r.status_code}. text: {r._content}. method: {method}')
            raise Exception(f'status not 2xx. status code: {r.status_code}')
        try:
            if r is None or len(r.content) == 0:
                return method.response_process({})
            return method.response_process(r.json())
        except Exception as e:
            logging.info(f'not a json response: {e}')
            return method.response_process({})
