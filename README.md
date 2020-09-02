# Python-clients

This library implements wrapper for different python interfaces. We have:

* sync and async http client (requests and aiohttp libraries)

Each client is class with request method and class implemented base class of any custom methods. This is very simple. 
But you can encapsulate inner structure of requests.

# Installation

We use python3.7. Installation is a very simple:

    pip install python-clients
    
# Example

You define new client for specify endpoint: 

    client = http.AsyncClient(url)

Next, you define the first method:

    class MyCustomFirstMethod(http.Method):
        url _ = '/'
        m_type = 'POST'

Next, you define the second method:

    class MyCustomSecondMethod(http.Method):
        url _ = '/%s'
        count = 1
        m_type = 'POST'
        
        def __init __ (self, arg1, arg2, arg3):
            http.Method. __init __ (self, arg1)  # arg1 pass into self.url _ by position
            self.params = {'args1': arg1}
            self.body = {'arg2': arg2}
            

Next, you can take request:

    m = MyCustomFirstMethod()
    resp, status_code = await client.request(m)
    assert status_code == 200
    m = MyCustomSecondMethod(arg1=1, arg2=2, arg3=3)
    resp, status_code = await client.request(m)
    assert status_code == 204
    
    
# Development

You can install development requirements:

    pip install -r requirements/dev
    
This is extension of package version of requirements

# Test

Before tests, you need to start mock server:

    PYTHONPATH=. python tests/server/mock_server.py

After that, you can run all tests:

    pytest tests
