import copy

import pytest

from clients import http


class TestException(Exception):
    pass


class Response:
    def __init__(self, response, content, status_code):
        self.response = response
        self.status_code = status_code
        self.content = content

    def json(self):
        return {'response': self.response}


class MockRequests:
    def __init__(self, resp, content, code, failure=False):
        self.response = Response(response=resp, status_code=code, content=content)
        self.failure = failure

    def __failure(self):
        raise TestException()

    def get(self, **args):
        if self.failure:
            self.__failure()
        return self.response

    def post(self, **args):
        if self.failure:
            self.__failure()
        return self.response

    def delete(self, **args):
        if self.failure:
            self.__failure()
        return self.response

    def files(self, **kwargs):
        assert 'files' in kwargs
        if self.failure:
            self.__failure()
        return self.response

    def patch(self, **args):
        if self.failure:
            self.__failure()
        return self.response

    def put(self, **args):
        if self.failure:
            self.__failure()
        return self.response


fake_url = 'https://ed.cba'
real_url = 'https://yandex.ru'


class GetResponseProcess(http.Method):
    url_ = '/'
    m_type = 'GET'

    def response_process(self, resp, status_code):
        return None, 200


class Get(http.Method):
    url_ = '/'
    m_type = 'GET'


class GetWithBody(http.Method):
    url_ = '/'
    m_type = 'GET'
    body = {}


class Post(http.Method):
    url_ = '/'
    m_type = 'POST'
    body = {}


class Put(http.Method):
    url_ = '/'
    m_type = 'PUT'
    body = {}


class Patch(http.Method):
    url_ = '/'
    m_type = 'PATCH'
    body = {}


class File(http.Method):
    url_ = '/'
    m_type = 'FILE'
    files = {}


class FileNoFileField(http.Method):
    url_ = '/'
    m_type = 'FILE'


class Undefined(http.Method):
    url_ = '/'
    m_type = '#'
    body = {}


class Delete(http.Method):
    url_ = '/'
    m_type = 'DELETE'
    body = {}


def test_request_get_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(Get())
    assert resp == {}
    assert status_code == 204


def test_request_get_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(TestException):
        client.request(Get())


def test_request_get_body_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(AssertionError):
        client.request(GetWithBody())


def test_request_post_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(Post())
    assert resp == {}
    assert status_code == 204


def test_request_post_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(TestException):
        client.request(Post())


def test_request_put_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(Put())
    assert resp == {}
    assert status_code == 204


def test_request_put_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(TestException):
        client.request(Put())


def test_request_patch_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(Patch())
    assert resp == {}
    assert status_code == 204


def test_request_patch_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(TestException):
        client.request(Patch())


def test_request_files_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(File())
    assert resp == {}
    assert status_code == 204


def test_request_files_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(TestException):
        client.request(File())


def test_request_files_without_files():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(FileNoFileField())
    assert resp == {}
    assert status_code == 204


def test_request_delete_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(Delete())
    assert resp == {}
    assert status_code == 204


def test_request_delete_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(TestException):
        client.request(Delete())


def test_request_undefined():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(fake_url)
    with pytest.raises(NotImplementedError):
        client.request(Undefined())


def test_response_process():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url)
    resp, status_code = client.request(GetResponseProcess())
    assert resp is None
    assert status_code == 200


def test_real_request():
    # Mock requests
    import requests
    http.requests = requests

    client = http.Client(real_url)
    resp, status_code = client.request(Get())
    assert len(resp) > 1000
    assert status_code == 200


def middleware(m):
    m_ = copy.deepcopy(m)
    m_.headers = {'test': 'test'}
    return m_


def test_request_mdws():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url, mdws=[middleware])
    m = Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert Get().__dict__ == m.__dict__
    assert status_code == 204


def middleware_not_copy(m):
    m.headers = {'test': 'test'}
    return m


def test_request_mdws_not_copy():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url, mdws=[middleware_not_copy])
    m = Get()
    with pytest.raises(AssertionError):
        client.request(m)


def test_request_mdws_nc():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url, mdws_nc=[middleware])
    m = Get()
    with pytest.raises(AssertionError):
        client.request(m)


def test_request_mdws_nc_not_copy():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(fake_url, mdws_nc=[middleware_not_copy])
    m = Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert Get().__dict__ != m.__dict__
    assert status_code == 204
