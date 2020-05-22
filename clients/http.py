import json
import logging
import typing

import aiohttp
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
    files = None
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
        except:
            r_ = r.content
        try:
            if r_ is None or len(r.content) == 0:
                return method.response_process({}, r.status_code)
            return method.response_process(r_, r.status_code)
        except Exception as e:
            logging.info(f'not a json response: {e}')
            return method.response_process({}, 520)
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

    @property
    def body_(self):
        if self.body is None:
            return None
        return json.dumps(self.body)


middleware_type_ = typing.List[typing.Callable[[Method], Method]]


class AsyncClient:
    def __init__(self, endpoint: str, mdws: middleware_type_ = None,
                 mdws_nc: middleware_type_ = None):
        """
        This client implements http-client

        :param endpoint: base url for requests
        :param mdws: (middlewares) list of middlewares of methods. After calling source object of method is changed.
                     This case more slowly, than mdws_nc. You must select mdws or mdws_nc
            For example, you need add functionality for each methods. You can add the only argument to the constructor
            of client. For example, you have 200 places with calling some method (in tests, for example), than, you can
            add middleware in the only place.
        :param mdws_nc: (middlewares not copy) list of middlewares of methods. After calling source object of method is
                        changed. This case more faster, than mdws. You must select mdws or mdws_nc
        """
        self.endpoint = endpoint
        a = mdws is not None and mdws_nc is None
        b = mdws is None and mdws_nc is not None
        c = mdws is None and mdws_nc is None
        assert a or b or c, 'you must set mdws or mdws_nc, but not both'
        self.mdws = []
        if mdws is not None:
            self.mdws = mdws
        self.mdws_nc = []
        if mdws_nc is not None:
            self.mdws_nc = mdws_nc
        self.__session = None

    def __get_url(self, method):
        return f'{self.endpoint}{method.url}'

    def __middlewares(self, method_):
        method = method_
        for m in self.mdws:
            method_ = m(method)
            assert id(method_) != id(method), 'middleware must call copy for argument of method before ' \
                                              'return: return copy.copy(m). See test test_request_middleware and ' \
                                              'test_request_middleware_not_copy for example. If you want to use ' \
                                              'middleware without copy, you need, mdws_nc argument in constructor'
            method = method_
        for m in self.mdws_nc:
            method_ = m(method)
            assert id(method_) == id(method), 'middleware must NOT call copy for argument of method. See test ' \
                                              'test_request_middleware and test_request_middleware_not_copy for ' \
                                              'example. If you want to use middleware with copy, you need, ' \
                                              'mdws argument in constructor'
            method = method_
        return method

    async def resolve(self):
        if self.__session is None:
            return
        await self.__session.close()

    async def request(self, method: Method, proxy: str = None):
        """
        requests is used to take a request by url asynchronously

        :param method: object of method
        :param proxy: is url of proxy (example: http://proxy.com)
        :return:
        """
        if self.__session is None:
            self.__session = aiohttp.ClientSession()
        # TODO: two steps requests: 1. take headers; 2. take body (text or json)
        # TODO: add task to running event loop
        method = self.__middlewares(method)
        params = method.params
        body = method.body_
        headers = method.headers
        m_type = method.m_type.lower()
        auth_ = method.auth
        proxy = proxy if proxy is not None else None
        files = method.files if method.files is not None else None
        url = self.__get_url(method)
        assert files is None, "files files is not supported. please use {'file': open('file', 'rb')} and pass data"
        if m_type == 'get':
            assert body is None, 'for GET method body must be empty'
        resp = await self.__session.request(method=m_type, url=url, params=params, data=body, headers=headers,
                                            proxy=proxy, auth=auth_)
        try:
            r_ = await resp.json()
        except:
            r_ = await resp.text()
        try:
            return method.response_process(r_, resp.status)
        except Exception as e:
            logging.info(f'not a json response: {e}')
            return method.response_process({}, 520)


class Client:
    def __init__(self, endpoint: str, proxies: list = None, mdws: middleware_type_ = None,
                 mdws_nc: middleware_type_ = None):
        """
        This client implements http-client

        :param endpoint: base url for requests
        :param proxies: dict with proxies ({'schema': 'endpoint'})
        :param mdws: (middlewares) list of middlewares of methods. After calling source object of method is changed.
                     This case more slowly, than mdws_nc. You must select mdws or mdws_nc
            For example, you need add functionality for each methods. You can add the only argument to the constructor
            of client. For example, you have 200 places with calling some method (in tests, for example), than, you can
            add middleware in the only place.
        :param mdws_nc: (middlewares not copy) list of middlewares of methods. After calling source object of method is
                        changed. This case more faster, than mdws. You must select mdws or mdws_nc
        """
        self.endpoint = endpoint
        self.proxies = proxies
        a = mdws is not None and mdws_nc is None
        b = mdws is None and mdws_nc is not None
        c = mdws is None and mdws_nc is None
        assert a or b or c, 'you must set mdws or mdws_nc, but not both'
        self.mdws = []
        if mdws is not None:
            self.mdws = mdws
        self.mdws_nc = []
        if mdws_nc is not None:
            self.mdws_nc = mdws_nc

    def __get_url(self, method):
        return f'{self.endpoint}{method.url}'

    def __middlewares(self, method_):
        method = method_
        for m in self.mdws:
            method_ = m(method)
            assert id(method_) != id(method), 'middleware must call copy for argument of method before ' \
                                              'return: return copy.copy(m). See test test_request_middleware and ' \
                                              'test_request_middleware_not_copy for example. If you want to use ' \
                                              'middleware without copy, you need, mdws_nc argument in constructor'
            method = method_
        for m in self.mdws_nc:
            method_ = m(method)
            assert id(method_) == id(method), 'middleware must NOT call copy for argument of method. See test ' \
                                              'test_request_middleware and test_request_middleware_not_copy for ' \
                                              'example. If you want to use middleware with copy, you need, ' \
                                              'mdws argument in constructor'
            method = method_
        return method

    def request(self, method):
        method = self.__middlewares(method)
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
            raise NotImplementedError("\nnot implemented method request: %s" % method.m_type)
        try:
            r_ = r.json()
        except:
            r_ = r.content
        try:
            if r_ is None or len(r.content) == 0:
                return method.response_process({}, r.status_code)
            return method.response_process(r_, r.status_code)
        except Exception as e:
            logging.info(f'not a json response: {e}')
            return method.response_process({}, 520)
