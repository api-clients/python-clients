from clients import http

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
