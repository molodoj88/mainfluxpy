from mainflux.api_request import GetRequest, PostRequest


class TestRequests:
    """Tests of requests from mainflux.api_request"""
    def test_get_request(self):
        """
        GetRequest entity call should return response with status code 200.
        """
        test_url = 'http://httpbin.org/get'
        request = GetRequest(url=test_url)
        response = request()
        assert str(response.status_code) == '200'

    def test_get_request_with_params(self):
        """
        GetRequest entity with params provided should make GET request
        with http parameters. If we provide params as dict like that:
        {
            'param1': 'param1',
            'param2': 'param2'
        }
        and url, for example, 'http://httpbin.org/anything',
        call on GetRequest entity should make GET request on url:
        'http://httpbin.org/anything?param1=param1&param2=param2'
        """
        test_url = 'http://httpbin.org/anything'
        params = {'param1': 'param1', 'param2': 'param2'}
        request = GetRequest(url=test_url, params=params)
        response = request()
        json = response.json()
        for k, v in params.items():
            assert json['args'][k] == v

    def test_post_request_with_params(self):
        test_url = 'http://httpbin.org/anything'
        params = {"param1": "param1", "param2": "param2"}
        request = PostRequest(url=test_url, params=params)
        response = request()
        json = response.json()
        assert str(response.status_code) == '200'
        assert json['method'] == 'POST'
        for k, v in params.items():
            assert json['args'][k] == v

    def test_post_request_with_data(self):
        """
        PostRequest call with provided 'json' parameter.
        The response must contain the data sent.
        """
        test_url = 'http://httpbin.org/anything'
        data = {'data1': 'somedata1', 'data2': 'somedata2'}
        request = PostRequest(url=test_url, json=data)
        response = request()
        json = response.json()
        assert str(response.status_code) == '200'
        assert json['method'] == 'POST'
        assert json['json'] == data

    def test_post_request_with_headers(self):
        """
        By default, the "Content-Type: application/json" header
        is added to all requests. We also check the addition
        of an arbitrary header to the request.
        The response should contain all sent headers.
        """
        test_url = 'http://httpbin.org/anything'
        headers = {'Some-Custom-Header': 'Custom header value'}
        request = PostRequest(url=test_url, headers=headers)
        response = request()
        json = response.json()
        assert str(response.status_code) == '200'
        assert json['method'] == 'POST'
        assert json['headers']['Content-Type'] == 'application/json'
        assert json['headers']['Some-Custom-Header'] == 'Custom header value'
