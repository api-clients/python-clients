import copy
from pathlib import Path
import pytest

from tests import unit, port
from clients import http

req = http.requests


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
        return self.response

    async def text(self):
        if self.json_:
            raise Exception()
        return self.content


class MockSessions:
    def __init__(self, resp, content, code, failure=False, json_=True):
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
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=False)
    resp, status_code = await client.request(unit.Get())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_get_failure():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(http.RequestException):
        await client.request(unit.Get())


@pytest.mark.asyncio
async def test_request_get_body_failure():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(AssertionError):
        await client.request(unit.GetWithBody())


@pytest.mark.asyncio
async def test_request_post_ok():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    resp, status_code = await client.request(unit.Post())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_post_failure():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(http.RequestException):
        await client.request(unit.Post())


@pytest.mark.asyncio
async def test_request_put_ok():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    resp, status_code = await client.request(unit.Put())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_put_failure():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(http.RequestException):
        await client.request(unit.Put())


@pytest.mark.asyncio
async def test_request_patch_ok():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    resp, status_code = await client.request(unit.Patch())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_patch_failure():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(http.RequestException):
        await client.request(unit.Patch())


@pytest.mark.asyncio
async def test_request_files_ok():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    m = unit.File()
    m.files = None
    resp, status_code = await client.request(m)
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_multiple_files_ok():
    # Mock requests
    # http.requests = MockRequests(resp=None, code=204, content='')
    http.requests = req
    src_path = Path.cwd().joinpath("tests", "data")
    f_json = 'data_file1.json'
    f1 = 'data_file1.txt'
    f2 = 'data_file2.txt'
    multiple_files = [http.AsyncFile('files', open(src_path.joinpath(f_json), 'rb'), f_json, 'application/json'),
                      http.AsyncFile('files', open(src_path.joinpath(f1), 'rb'), f1, None),
                      http.AsyncFile('files', open(src_path.joinpath(f2), 'rb'), f2, None),
                      ]

    client = http.AsyncClient(f"http://localhost:{port}")
    resp, status_code = await client.request(unit.ManyFilesAsync(multiple_files))
    assert resp == {'success': True}
    assert status_code == 200


@pytest.mark.asyncio
async def test_request_multiple_files_and_data_ok():
    # Mock requests
    # http.requests = MockRequests(resp=None, code=204, content='')
    http.requests = req
    src_path = Path.cwd().joinpath("tests", "data")
    f_json = 'data_file1.json'
    f1 = 'data_file1.txt'
    f2 = 'data_file2.txt'
    multiple_files = [http.AsyncFile('files', open(src_path.joinpath(f_json), 'rb'), f_json, 'application/json'),
                      http.AsyncFile('files', open(src_path.joinpath(f1), 'rb'), f1, None),
                      http.AsyncFile('files', open(src_path.joinpath(f2), 'rb'), f2, None),
                      ]

    client = http.AsyncClient(f"http://localhost:{port}")
    resp, status_code = await client.request(
        unit.ManyFilesAndDataAsync(multiple_files, body={"data1": "data1", "data2": 12345}))
    assert resp == {'success': True}
    assert status_code == 200


@pytest.mark.asyncio
async def test_request_data_ok():
    # Mock requests
    # http.requests = MockRequests(resp=None, code=204, content='')
    http.requests = req
    data = {"data1": "data1",
            "data2": 12345,
            "data3": False
            }

    client = http.AsyncClient(f"http://localhost:{port}")
    resp, status_code = await client.request(unit.DataDict(data))
    assert resp == {'success': True}
    assert status_code == 200


@pytest.mark.asyncio
async def test_request_files_failure():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(http.RequestException):
        m = unit.File()
        m.files = None
        await client.request(m)


@pytest.mark.asyncio
async def test_request_delete_ok():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    resp, status_code = await client.request(unit.Delete())
    assert resp == {}
    assert status_code == 204


@pytest.mark.asyncio
async def test_request_delete_failure():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(http.RequestException):
        await client.request(unit.Delete())


@pytest.mark.asyncio
async def test_request_undefined():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='', failure=True)
    with pytest.raises(http.RequestException):
        await client.request(unit.Undefined())


@pytest.mark.asyncio
async def test_response_process():
    client = http.AsyncClient(unit.fake_url)
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    resp, status_code = await client.request(unit.GetResponseProcess())
    assert resp is None
    assert status_code == 200


@pytest.mark.asyncio
async def test_real_request():
    client = http.AsyncClient(unit.real_url)
    resp, status_code = await client.request(unit.Get())
    assert len(resp) > 1000
    assert status_code == 200


@pytest.mark.asyncio
async def test_real_request_global_client():
    resp, status_code = await unit.client.request(unit.Get())
    assert len(resp) > 1000
    assert status_code == 200


def middleware(m):
    m_ = copy.deepcopy(m)
    m_.headers = {'test': 'test'}
    return m_


@pytest.mark.asyncio
async def test_request_mdws():
    client = http.AsyncClient(unit.fake_url, mdws=[middleware])
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    m = unit.Get()
    resp, status_code = await client.request(m)
    assert resp == {}
    assert unit.Get().__dict__ == m.__dict__
    assert status_code == 204


def middleware_not_copy(m):
    m.headers = {'test': 'test'}
    return m


@pytest.mark.asyncio
async def test_request_mdws_not_copy():
    client = http.Client(unit.fake_url, mdws=[middleware_not_copy])
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    m = unit.Get()
    with pytest.raises(AssertionError):
        client.request(m)


@pytest.mark.asyncio
async def test_request_mdws_nc():
    client = http.Client(unit.fake_url, mdws_nc=[middleware])
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    m = unit.Get()
    with pytest.raises(AssertionError):
        client.request(m)


@pytest.mark.asyncio
async def test_request_mdws_nc_not_copy():
    client = http.AsyncClient(unit.fake_url, mdws_nc=[middleware_not_copy])
    client._AsyncClient__session = MockSessions(resp={}, code=204, content='')
    m = unit.Get()
    resp, status_code = await client.request(m)
    assert resp == {}
    assert unit.Get().__dict__ != m.__dict__
    assert status_code == 204
