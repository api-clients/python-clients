import copy

import pytest

from tests import unit
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


def test_request_get_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.Get())
    assert resp == {}
    assert status_code == 204


def test_request_get_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(TestException):
        client.request(unit.Get())


def test_request_get_body_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(AssertionError):
        client.request(unit.GetWithBody())


def test_request_post_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.Post())
    assert resp == {}
    assert status_code == 204


def test_request_post_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(TestException):
        client.request(unit.Post())


def test_request_put_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.Put())
    assert resp == {}
    assert status_code == 204


def test_request_put_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(TestException):
        client.request(unit.Put())


def test_request_patch_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.Patch())
    assert resp == {}
    assert status_code == 204


def test_request_patch_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(TestException):
        client.request(unit.Patch())


def test_request_files_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.File())
    assert resp == {}
    assert status_code == 204


def test_request_files_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(TestException):
        client.request(unit.File())


def test_request_files_without_files():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.FileNoFileField())
    assert resp == {}
    assert status_code == 204


def test_request_delete_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.Delete())
    assert resp == {}
    assert status_code == 204


def test_request_delete_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(TestException):
        client.request(unit.Delete())


def test_request_undefined():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(unit.fake_url)
    with pytest.raises(NotImplementedError):
        client.request(unit.Undefined())


def test_response_process():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url)
    resp, status_code = client.request(unit.GetResponseProcess())
    assert resp is None
    assert status_code == 200


def test_real_request():
    # Mock requests
    import requests
    http.requests = requests

    client = http.Client(unit.real_url)
    resp, status_code = client.request(unit.Get())
    assert len(resp) > 1000
    assert status_code == 200


def middleware(m):
    m_ = copy.deepcopy(m)
    m_.headers = {'test': 'test'}
    return m_


def test_request_mdws():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url, mdws=[middleware])
    m = unit.Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert unit.Get().__dict__ == m.__dict__
    assert status_code == 204


def middleware_not_copy(m):
    m.headers = {'test': 'test'}
    return m


def test_request_mdws_not_copy():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url, mdws=[middleware_not_copy])
    m = unit.Get()
    with pytest.raises(AssertionError):
        client.request(m)


def test_request_mdws_nc():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url, mdws_nc=[middleware])
    m = unit.Get()
    with pytest.raises(AssertionError):
        client.request(m)


def test_request_mdws_nc_not_copy():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(unit.fake_url, mdws_nc=[middleware_not_copy])
    m = unit.Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert unit.Get().__dict__ != m.__dict__
    assert status_code == 204
