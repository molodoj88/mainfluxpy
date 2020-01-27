"""
Tests for api functions
"""
import pytest
from .common import THINGS_TO_DELETE, CHANNELS_TO_DELETE
import random


class TestApiToken:
    def test_get_token(self, app):
        token = app.api.token
        assert isinstance(token, str)
        assert len(token) > 0


@pytest.mark.usefixtures('clean_things')
class TestThingsApi:
    BULK_CREATION_NUMBER = 5

    @staticmethod
    def create_thing(name, app):
        return app.api.create_thing(name)

    def test_delete_all_things(self, app):
        thing_names = [str(i) for i in range(10)]
        things = app.api.create_things_bulk(thing_names)
        assert len(things) == len(thing_names)
        app.api.delete_all_things()
        things = app.api.get_things()
        assert things == []

    def test_thing_creation(self, app, random_thing_name):
        test_name = random_thing_name()
        thing_id = self.create_thing(test_name, app)
        THINGS_TO_DELETE.append(thing_id)
        assert thing_id is not None

    def test_thing_bulk_creation(self, app, random_thing_name):
        names = [random_thing_name() for i in range(self.BULK_CREATION_NUMBER)]
        things = app.api.create_things_bulk(names)
        THINGS_TO_DELETE.extend([t['id'] for t in things])
        assert isinstance(things, list)
        created_names = [t['name'] for t in things]
        for name in names:
            assert name in created_names

    def test_thing_deletion(self, app):
        _id = random.choice(THINGS_TO_DELETE)
        status_code = app.api.delete_thing(_id)
        assert status_code == 204
        THINGS_TO_DELETE.remove(_id)

    def test_get_things(self, app):
        things = app.api.get_things()
        assert isinstance(things, list)
        assert things
        assert set(THINGS_TO_DELETE).issubset(set([t['id'] for t in things]))

    def test_get_thing(self, app, random_thing_name):
        name = random_thing_name()
        _id = self.create_thing(name, app)
        assert isinstance(_id, str)
        THINGS_TO_DELETE.append(_id)
        thing = app.api.get_thing(_id)
        assert isinstance(thing, dict)
        assert thing['id'] == _id
        assert thing['name'] == name


@pytest.mark.usefixtures('clean_channels')
class TestChannelsApi:
    BULK_CREATION_NUMBER = 5

    @staticmethod
    def create_channel(name, app):
        return app.api.create_channel(name)

    def test_delete_all_channels(self, app):
        channels_names = [str(i) for i in range(10)]
        channels = app.api.create_channels_bulk(channels_names)
        assert len(channels) == len(channels_names)
        app.api.delete_all_channels()
        channels = app.api.get_channels()
        assert channels == []
