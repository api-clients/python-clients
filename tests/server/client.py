from clients import http


class Post(http.Method):
    url_ = '/method'
    m_type = 'POST'


class Get(http.Method):
    url_ = '/method'
    m_type = 'GET'


class FileRequest(http.Method):
    url_ = '/raise'
    m_type = 'POST'


class FileResponse(http.Method):
    url_ = '/file:request'
    m_type = 'POST'
