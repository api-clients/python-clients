import io

import pytest

import tests
from clients import http
from tests.server import client


def test_get():
    client_ = http.Client(f'http://localhost:{tests.port}')
    m = client.Get()
    resp, status_code = client_.request(m)
    assert status_code == 200


def test_post():
    client_ = http.Client(f'http://localhost:{tests.port}')
    m = client.Post()
    resp, status_code = client_.request(m)
    assert status_code == 200


def test_raise():
    client_ = http.Client(f'http://localhost:{tests.port}')
    m = client.Raise()
    resp, status_code = client_.request(m)
    assert status_code == 400


@pytest.mark.asyncio
async def test_file_async_request():
    client_ = http.AsyncClient(f'http://localhost:{tests.port}')
    m = client.AsyncFileRequest(io.StringIO('123'))
    resp, status_code = await client_.request(m)
    assert status_code == 200


@pytest.mark.asyncio
async def test_file_sync_request():
    client_ = http.Client(f'http://localhost:{tests.port}')
    m = client.SyncFileRequest(io.StringIO('123'))
    resp, status_code = client_.request(m)
    assert status_code == 200


@pytest.mark.asyncio
async def test_file_async_response():
    client_ = http.AsyncClient(f'http://localhost:{tests.port}')
    m = client.AsyncFileResponse(io.StringIO('123a'))
    resp, status_code = await client_.request(m)
    assert status_code == 200
    assert type(resp) == bytes


@pytest.mark.asyncio
async def test_file_sync_response():
    client_ = http.Client(f'http://localhost:{tests.port}')
    m = client.SyncFileResponse(io.StringIO('123a'))
    resp, status_code = client_.request(m)
    assert status_code == 200
    assert type(resp) == bytes
