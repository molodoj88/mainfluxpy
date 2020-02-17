from mainflux.app import MainfluxApp
import pytest
import uuid
import requests
import httpx
from .common import THINGS_TO_DELETE, CHANNELS_TO_DELETE, APP


class TestManager:

    app = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TestManager, cls).__new__(cls)
        return cls.instance


@pytest.fixture(scope='module')
def app():
    app = MainfluxApp()
    print(f"Api token: {app.api.token}")
    test_manager = TestManager()
    test_manager.app = app
    return app


@pytest.fixture(scope='module')
def http_client():
    client = httpx.Client()
    yield client
    client.close()


@pytest.fixture
def random_thing_name():
    def make_random_name():
        return str(uuid.uuid4())
    return make_random_name


@pytest.fixture(scope='module')
def clean_things():
    yield
    app = TestManager().app
    for thing in THINGS_TO_DELETE:
        app.api.delete_thing(thing)


@pytest.fixture(scope='module')
def clean_channels():
    yield
    app = TestManager().app
    for channel in CHANNELS_TO_DELETE:
        app.api.delete_thing(channel)
