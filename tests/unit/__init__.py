from clients import http
import typing

fake_url = 'https://ed.cba'
real_url = 'https://yandex.ru'

client = http.AsyncClient(real_url)


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
    files_sync = {}


class ManyFiles(http.Method):
    url = "/manyfiles"
    m_type = "FILE"
    auth = None

    def __init__(self, files):  # typing.List):
        http.Method.__init__(self)
        self.files_sync = files


class ManyFilesAsync(http.Method):
    url = "/manyfiles"
    m_type = "FILE"
    auth = None

    def __init__(self, files):  # typing.List):
        http.Method.__init__(self)
        self.files_async = files


class ManyFilesAndData(http.Method):
    url = "/manyfilesanddata"
    m_type = "FILE"
    auth = None

    def __init__(self, files, body=None):  # typing.List):
        http.Method.__init__(self)
        self.body = body
        self.files_sync = files


class ManyFilesAndDataAsync(http.Method):
    url = "/manyfilesanddata"
    m_type = "FILE"
    auth = None

    def __init__(self, files, body=None):  # typing.List):
        http.Method.__init__(self)
        self.body = body
        self.files_async = files


class DataDict(http.Method):
    url_ = "/datadict"
    m_type = "POST"
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
    }

    def __init__(self, data: typing.Dict):
        http.Method.__init__(self)
        # assert len(users) > 0, 'you must pass any users'
        # assert isinstance(users, list), ' users must be list with any dicts'
        self.body = data


class FileNoFileField(http.Method):
    url_ = '/'
    m_type = 'FILE'
    files_sync = {}


class Undefined(http.Method):
    url_ = '/'
    m_type = '#'
    body = {}


class Delete(http.Method):
    url_ = '/'
    m_type = 'DELETE'
    body = {}
