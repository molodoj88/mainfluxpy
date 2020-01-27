from mainflux.app import MainfluxApp
import pytest
import uuid
from .common import THINGS_TO_DELETE, CHANNELS_TO_DELETE

APP = MainfluxApp()


@pytest.fixture(scope='module')
def app():
    return APP


@pytest.fixture
def random_thing_name():
    def make_random_name():
        return str(uuid.uuid4())
    return make_random_name


@pytest.fixture(scope='module')
def clean_things():
    yield
    for thing in THINGS_TO_DELETE:
        APP.api.delete_thing(thing)


@pytest.fixture(scope='module')
def clean_channels():
    yield
    for channel in CHANNELS_TO_DELETE:
        APP.api.delete_thing(channel)
