import copy
import time

import pytest

import tests
from clients import http


class TestException(Exception):
    pass


class Response:
    def __init__(self, response, content, status, json_):
        self.response = response
        self.status = status
        self.content = content
        self.json_ = json_

    async def json(self):
        if not self.json_:
            raise Exception()
        return {'response': self.response}

    async def text(self):
        if self.json_:
            raise Exception()
        return {'response': self.response}


class MockSessions:
    def __init__(self, resp, content, code, failure=False, json_=False):
        self.response = Response(response=resp, status=code, content=content, json_=json_)
        self.failure = failure

    def __failure(self):
        raise TestException()

    async def request(self, **args):
        if self.failure:
            self.__failure()
        return self.response


@pytest.mark.asyncio
async def test_request_get_ok():
    client = http.AsyncClient(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='', failure=False)
    resp, status_code = await client.request(tests.Get())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_get_failure():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='', failure=True)
    with pytest.raises(TestException):
        await client.request(tests.Get())


@pytest.mark.asyncio
async def test_request_get_body_failure():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='', failure=True)
    with pytest.raises(AssertionError):
        await client.request(tests.GetWithBody())


@pytest.mark.asyncio
async def test_request_post_ok():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='')
    resp, status_code = await client.request(tests.Post())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_post_failure():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='')
    with pytest.raises(TestException):
        await client.request(tests.Post())


@pytest.mark.asyncio
async def test_request_put_ok():
    client = http.AsyncClient(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='')
    resp, status_code = await client.request(tests.Put())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_put_failure():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='')
    with pytest.raises(TestException):
        await client.request(tests.Put())


@pytest.mark.asyncio
async def test_request_patch_ok():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='')
    resp, status_code = await client.request(tests.Patch())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_patch_failure():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='')
    with pytest.raises(TestException):
        client.request(tests.Patch())


@pytest.mark.asyncio
async def test_request_files_ok():
    client = http.Client(tests.fake_url)
    client._AsyncClient__session = MockSessions(resp=None, code=204, content='')
    resp, status_code = client.request(tests.File())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_files_failure():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.File())


@pytest.mark.asyncio
async def test_request_files_without_files():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.FileNoFileField())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_delete_ok():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.Delete())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_delete_failure():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(TestException):
        client.request(tests.Delete())


@pytest.mark.asyncio
async def test_request_undefined():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='', failure=True)

    client = http.Client(tests.fake_url)
    with pytest.raises(NotImplementedError):
        client.request(tests.Undefined())


@pytest.mark.asyncio
async def test_response_process():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='')

    client = http.Client(tests.fake_url)
    resp, status_code = client.request(tests.GetResponseProcess())
    assert resp is None
    assert status_code == 200


@pytest.mark.asyncio
async def test_real_request():
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


@pytest.mark.asyncio
async def test_request_mdws():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws=[middleware])
    m = tests.Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert tests.Get().__dict__ == m.__dict__
    assert status_code == 204


def middleware_not_copy(m):
    m.headers = {'test': 'test'}
    return m


@pytest.mark.asyncio
async def test_request_mdws_not_copy():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws=[middleware_not_copy])
    m = tests.Get()
    with pytest.raises(AssertionError):
        client.request(m)


@pytest.mark.asyncio
async def test_request_mdws_nc():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws_nc=[middleware])
    m = tests.Get()
    with pytest.raises(AssertionError):
        client.request(m)


@pytest.mark.asyncio
async def test_request_mdws_nc_not_copy():
    # Mock requests
    http.requests = MockSessions(resp=None, code=204, content='')

    client = http.Client(tests.fake_url, mdws_nc=[middleware_not_copy])
    m = tests.Get()
    resp, status_code = client.request(m)
    assert resp == {}
    assert tests.Get().__dict__ != m.__dict__
    assert status_code == 204
