from typing import Dict
import requests


class ApiRequest:
    def __init__(self, url: str = "", params: Dict = None, json: Dict = None, headers: Dict = None):
        self._url = url
        self._headers = {"Content-Type": "application/json"}
        if headers:
            self.update_headers(headers)
        self._params = params or {}
        self._json = json or {}
        # In subclass we should provide method name (func name from requests)
        self.method = ""

    def _execute(self):
        method = self.method
        func = getattr(requests, method)
        kwargs = {"headers": self._headers}
        if self._params:
            kwargs["params"] = self._params
        if self._json:
            kwargs["json"] = self._json
        return func(self._url, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._execute()

    def update_params(self, params: dict):
        self._params.update(params)

    def update_headers(self, headers: dict):
        self._headers.update(headers)


class GetRequest(ApiRequest):
    """
    GET http method implementation
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "get"


class PostRequest(ApiRequest):
    """
    POST http method implementation
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "post"


class PutRequest(ApiRequest):
    """
    PUT http method implementation
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "put"


class DeleteRequest(ApiRequest):
    """
    DELETE http method implementation
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "delete"


class PatchRequest(ApiRequest):
    """
    PATCH http method implementation
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "patch"
