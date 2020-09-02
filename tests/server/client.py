from clients import http


class Raise(http.Method):
    url_ = '/raise'
    m_type = 'GET'


class Post(http.Method):
    url_ = '/method'
    m_type = 'POST'


class Get(http.Method):
    url_ = '/method'
    m_type = 'GET'


class AsyncFileRequest(http.Method):
    url_ = '/file:request'
    m_type = 'FILE'

    def __init__(self, file):
        http.Method.__init__(self)
        self.files_async = [
            http.AsyncFile('file', file, 'my_file', None)
        ]


class SyncFileRequest(http.Method):
    url_ = '/file:request'
    m_type = 'FILE'

    def __init__(self, file):
        http.Method.__init__(self)
        self.files_sync = {'file': file}


class AsyncFileResponse(http.Method):
    url_ = '/file:response'
    m_type = 'FILE'

    def __init__(self, file):
        http.Method.__init__(self)
        self.files_async = [
            http.AsyncFile('file', file, 'my_file', None)
        ]


class SyncFileResponse(http.Method):
    url_ = '/file:response'
    m_type = 'FILE'

    def __init__(self, file):
        http.Method.__init__(self)
        self.files_sync = {'file': file}
