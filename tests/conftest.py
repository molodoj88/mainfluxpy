from mainflux.app import MainfluxApp
import pytest
import uuid
import httpx
from .conf import APP_KWARGS

"""
You should create file named conf.py in same directory where tests run
and create dictionary APP_KWARGS with following content:
 
APP_KWARGS = {
    'url': "ip-to-mainflux",
    'port': "80",
    'user': "username",
    'password': "password"
}
"""


class TestManager:
    def __init__(self, **app_args):
        self.app = MainfluxApp(url=app_args['url'],
                               port=app_args['port'],
                               user_email=app_args['user'],
                               user_password=app_args['password'])

    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TestManager, cls).__new__(cls)
        return cls.instance


@pytest.fixture(scope='module')
def app():
    test_manager = TestManager(**APP_KWARGS)
    app = test_manager.app
    return app


@pytest.fixture(scope='module')
def http_client():
    client = httpx.Client()
    yield client
    client.close()


@pytest.fixture
def random_name():
    def make_random_name():
        return str(uuid.uuid4())
    return make_random_name


@pytest.fixture(scope='function', autouse=True)
def clean_things():
    yield
    app = TestManager(**APP_KWARGS).app
    app.api.delete_all_things()


@pytest.fixture(scope='function', autouse=True)
def clean_channels():
    yield
    app = TestManager(**APP_KWARGS).app
    app.api.delete_all_channels()
