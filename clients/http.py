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
    """
    :arg name: name of method 
    :arg type_: type of method (GET, POST, PUT etc...)
    :arg url: type of method (endpoint, for example: https://localhost:5000/api-docs. In this case is api-docs)
    :arg headers: headers for request
    :arg data: body of request
    :arg params: query params  
    :arg count: count params into path of url
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
    def __init__(self, endpoint):
        """
        This client implements http-client

        :param endpoint: base url for requests
        """
        self.endpoint = endpoint

    def __get_url(self, method):
        return f'{self.endpoint}{method.url}'

    def request(self, method):
        m_type = method.m_type
        url = self.__get_url(method)
        if m_type == 'GET':
            assert method.body is None, 'For GET method body must be empty'
            r = requests.get(url=url, params=method.params, headers=method.headers)
        elif m_type == 'POST':
            r = requests.post(url=url, params=method.params, data=method.body, headers=method.headers)
        elif m_type == 'DELETE':
            r = requests.delete(url=url, params=method.params, data=method.body, headers=method.headers)
        elif m_type == 'PATCH':
            r = requests.patch(url=url, params=method.params, data=method.body, headers=method.headers)
        else:
            raise Exception("\nnot implemented method request: %s" % method.m_type)

        if r.status_code // 100 != 2:
            logging.error(f'status code: {r.status_code}. text: {r._content}. method: {method}')
            raise Exception(f'status not 2xx. status code: {r.status_code}')
        if r is None:
            method.response_process({})
        return method.response_process(r.json())
