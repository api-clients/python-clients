import copy
import pytest

import tests
from python_clients import http

req = http.requests


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

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.Get())
    assert resp == {}
    assert status_code == 204


def test_request_get_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.Get())


def test_request_get_body_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(AssertionError):
        client.request(tests.GetWithBody())


def test_request_post_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.Post())
    assert resp == {}
    assert status_code == 204


def test_request_post_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.Post())


def test_request_put_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.Put())
    assert resp == {}
    assert status_code == 204


def test_request_put_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.Put())


def test_request_patch_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.Patch())
    assert resp == {}
    assert status_code == 204


def test_request_patch_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.Patch())


def test_request_files_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.File())
    assert resp == {}
    assert status_code == 204


def test_request_data_ok():
    http.requests = req
    data = {
        'data1': 'data1',
        'data2': 12345,
        'data3': False,
    }

    server_endpoint = f'{tests.server_schema}://{tests.server_host}:{tests.server_port}'
    client = http.Client(server_endpoint)
    resp, status_code = client.request(tests.DataDict(data))
    assert resp == {'success': True}
    assert status_code == 200


def test_request_multiple_files_and_data_ok():
    http.requests = req
    multiple_files = [
        ('files', (tests.f_json, open(tests.f_json, 'rb'), 'application/json')),
        ('files', (tests.f1_rst, open(tests.f1_rst, 'rb'))),
        ('files', (tests.f2_rst, open(tests.f2_rst, 'rb'))),
    ]

    client = http.Client(tests.server_endpoint)
    resp, status_code = client.request(
        tests.ManyFilesAndData(multiple_files, body={'data1': 'data1', 'data2': 12345}))
    assert resp == {'success': True}
    assert status_code == 200


def test_request_files_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.File())


def test_request_files_without_files():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.FileNoFileField())
    assert resp == {}
    assert status_code == 204


def test_request_delete_ok():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.Delete())
    assert resp == {}
    assert status_code == 204


def test_request_delete_failure():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.Delete())


def test_request_undefined():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(NotImplementedError):
        client.request(tests.Undefined())


def test_response_process():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.GetResponseProcess())
    assert resp is None
    assert status_code == 200


def test_real_request():
    # Mock requests
    import requests
    http.requests = requests

    client = http.Client(tests.real_url)
    resp, status_code = client.request(tests.Get())
    assert len(resp) > 1000
    assert status_code == 200


def middleware(m):
    m_ = copy.deepcopy(m)
    m_.headers = {'test': 'test'}
    return m_


def test_request_mdws():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws=[middleware])
    m = tests.Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert tests.Get().__dict__ == m.__dict__
    assert status_code == 204


def middleware_not_copy(m):
    m.headers = {'test': 'test'}
    return m


def test_request_mdws_not_copy():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws=[middleware_not_copy])
    m = tests.Get()
    with pytest.raises(AssertionError):
        client.request(m)


def test_request_mdws_nc():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws_nc=[middleware])
    m = tests.Get()
    with pytest.raises(AssertionError):
        client.request(m)


def test_request_mdws_nc_not_copy():
    # Mock requests
    http.requests = MockRequests(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws_nc=[middleware_not_copy])
    m = tests.Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert tests.Get().__dict__ != m.__dict__
    assert status_code == 204
