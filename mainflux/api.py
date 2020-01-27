from .api_request import GetRequest, PostRequest, DeleteRequest, PutRequest, PatchRequest
from typing import Iterable
from json.decoder import JSONDecodeError


def api_path(path):
    """
    Decorator to form full api method url
    :param path: str, api path
    :return: decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            url = self._prepare_url(path)
            return func(*args, **kwargs, url=url)
        return wrapper
    return decorator


class AbstractApi:
    def __init__(self, app=None):
        self._app = app
        self._address = self._app.config.MAINFLUX_URL
        self._token = None
        self.LIMIT = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    def _prepare_url(self, path: str):
        main_address = self._address
        if not path.startswith("/"):
            path = "/" + path
        return "{}{}".format(main_address, path)

    def _get_total(self, resource, request):
        response = request()
        try:
            json = response.json()
        except JSONDecodeError:
            return []
        _all: list = json[resource]
        _offset = self.LIMIT
        _total = json["total"]
        if _total > _offset:
            while _offset < _total:
                params = {"offset": _offset}
                request.update_params(params)
                response = request()
                _resource_list = response.json()[resource]
                _all.extend(_resource_list)
                _offset += self.LIMIT
        return _all

    def _create_resource(self, name, token=None, url=None):
        if not token:
            token = self._token
        headers = {"Authorization": token}
        data = {"name": name}
        request = PostRequest(url=url, json=data, headers=headers)
        response = request()
        resource_id = response.headers["Location"].split("/")[-1]
        return resource_id

    def _create_resource_bulk(self, resource, names: Iterable, token=None, url=None):
        if not token:
            token = self._token
        headers = {"Authorization": token}
        data = [{"name": name} for name in names]
        request = PostRequest(url=url, json=data, headers=headers)
        response = request()
        return response.json()[resource]

    def _delete_resource(self, resource_id, token=None, url=None):
        if not token:
            token = self._token
        url += "/{}".format(resource_id)
        headers = {"Authorization": token}
        request = DeleteRequest(url=url, headers=headers)
        response = request()
        return response.status_code


class UserApi(AbstractApi):
    @api_path("users")
    def create_user(self, username, password, url=None):
        """
        Create user
        :param url: url provided by @api_path decorator
        :param username: username
        :param password: password
        :return:
        """
        data = {"email": username, "password": password}
        request = PostRequest(url=url, json=data)
        response = request()
        return response.status_code


class ThingApi(AbstractApi):
    PATH = "things"

    @api_path(PATH)
    def get_things(self, name_pattern=None, token=None, url=None):
        token = token or self._token
        headers = {"Authorization": token}
        params = {"limit": self.LIMIT}
        request = GetRequest(url=url, params=params, headers=headers)
        if name_pattern:
            request.update_params({"name": name_pattern})
        things = self._get_total("things", request)
        return things

    @api_path(PATH)
    def get_thing(self, thing_id, token=None, url=None):
        token = token or self._token
        url += f"/{thing_id}"
        headers = {"Authorization": token}
        request = GetRequest(url=url, headers=headers)
        response = request()
        return response.json()

    @api_path(PATH)
    def get_connected_channels(self, thing_id, token=None, url=None):
        token = token or self._token
        url += f"/{thing_id}/channels"
        headers = {"Authorization": token}
        params = {"limit": self.LIMIT}
        request = GetRequest(url=url, params=params, headers=headers)
        channels = self._get_total("channels", request)
        return channels

    @api_path(PATH)
    def create_thing(self, name, token=None, url=None):
        if not name:
            raise AttributeError("You should provide name for new thing")
        thing_id = self._create_resource(name, token=token, url=url)
        return thing_id

    @api_path(f"{PATH}/bulk")
    def create_things_bulk(self, names: Iterable, token=None, url=None):
        if not names:
            raise AttributeError("You should provide names (iterable) for new things")
        things = self._create_resource_bulk("things", names=names, token=token, url=url)
        return things

    @api_path(PATH)
    def delete_thing(self, thing_id, token=None, url=None):
        status_code = self._delete_resource(thing_id, token=token, url=url)
        return status_code

    @api_path(PATH)
    def delete_all_things(self, token=None, url=None):
        token = token or self._token
        things = self.get_things()
        thing_ids = [t['id'] for t in things]
        if thing_ids:
            for thing_id in thing_ids:
                status_code = self._delete_resource(thing_id, token=token, url=url)
                # TODO Add log records for each deletion

    @api_path(PATH)
    def update_thing_key(self, thing_id, key, token=None, url=None):
        token = token or self._token
        url = f"{url}/{thing_id}/key"
        headers = {"Authorization": token}
        data = {"key": key}
        request = PatchRequest(url=url, headers=headers, json=data)
        response = request()
        return response.status_code


class ChannelApi(AbstractApi):
    PATH = "channels"

    @api_path(PATH)
    def get_channels(self, name_pattern=None, token=None, url=None):
        token = token or self._token
        headers = {"Authorization": token}
        params = {"limit": self.LIMIT}
        request = GetRequest(url=url, params=params, headers=headers)
        if name_pattern:
            request.update_params({"name": name_pattern})
        channels: Iterable = self._get_total("channels", request)
        return channels

    @api_path(PATH)
    def get_channel(self, channel_id, token=None, url=None):
        token = token or self._token
        url += f"/{channel_id}"
        headers = {"Authorization": token}
        request = GetRequest(url=url, headers=headers)
        response = request()
        return response.json()

    @api_path(PATH)
    def create_channel(self, name, token=None, url=None):
        channel_id = self._create_resource(name, token=token, url=url)
        return channel_id

    @api_path(f"{PATH}/bulk")
    def create_channels_bulk(self, names: Iterable, token=None, url=None):
        channels = self._create_resource_bulk("channels", names=names, token=token, url=url)
        return channels

    @api_path(PATH)
    def delete_channel(self, channel_id, token=None, url=None):
        status_code = self._delete_resource(channel_id, token=token, url=url)
        return status_code

    @api_path(PATH)
    def delete_all_channels(self, token=None, url=None):
        token = token or self._token
        channels = self.get_channels()
        channel_ids = [c['id'] for c in channels]
        if channel_ids:
            for channel_id in channel_ids:
                status_code = self._delete_resource(channel_id, token=token, url=url)
                # TODO Add log records for each deletion

    @api_path(PATH)
    def connect_thing_to_channel(self, channel_id, thing_id, token=None, url=None):
        token = token or self._token
        url += f"/{channel_id}/things/{thing_id}"
        headers = {"Authorization": token}
        request = PutRequest(url=url, headers=headers)
        response = request()
        return response.status_code

    @api_path(PATH)
    def disconnect_thing_from_channel(self, channel_id, thing_id, token=None, url=None):
        token = token or self._token
        url += f"/{channel_id}/things/{thing_id}"
        headers = {"Authorization": token}
        request = DeleteRequest(url=url, headers=headers)
        response = request()
        return response.status_code

    @api_path(PATH)
    def get_connected_things(self, channel_id, token=None, url=None):
        token = token or self._token
        url += f"/{channel_id}/things"
        headers = {"Authorization": token}
        params = {"limit": self.LIMIT}
        request = GetRequest(url=url, params=params, headers=headers)
        things = self._get_total("things", request)
        return things


class Api(ThingApi, ChannelApi, UserApi):
    """
    Provide Mainflux http API
    """
    def __init__(self, app):
        """
        :param app: MainfluxApp instance
        """
        super().__init__(app)
        # Corresponds to the "limit" parameter in requests to the
        # Mainflux http API, as, for example, described here:
        # https://mainflux.readthedocs.io/en/latest/provisioning/#retrieving-provisioned-things
        self.LIMIT = 100

    @api_path("tokens")
    def get_token(self, username=None, password=None, url=None):
        """
        Get auth token for making http requests
        :param url: url provided by @api_path decorator
        :param username: str, optionally (default is taken from settings.py)
        :param password: str, optionally (default is taken from settings.py)
        :return: str, token
        """
        if not (username or password):
            username = self._app.config.MAINFLUX_USER_EMAIL
            password = self._app.config.MAINFLUX_USER_PASSWORD
        data = {"email": username, "password": password}
        request = PostRequest(url=url, json=data)
        response = request()
        try:
            token = response.json()["token"]
        except Exception as e:
            print("Error:\n{}".format(e))
            return
        return token