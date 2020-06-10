"""
Tests for api functions
"""
import pytest


class TestApiToken:
    def test_get_token(self, app):
        token = app.api.token
        assert isinstance(token, str)
        assert len(token) > 0


@pytest.mark.usefixtures('clean_things')
class TestThingsApi:
    BULK_CREATION_NUMBER = 5

    def test_delete_all_things(self, app):
        thing_names = [str(i) for i in range(10)]
        things = app.api.create_things_bulk(thing_names)
        assert len(things) == len(thing_names)
        app.api.delete_all_things()
        things = app.api.get_things()
        assert things == []

    def test_thing_creation(self, app, random_name):
        thing_name = random_name()
        thing_id = app.api.create_thing(thing_name)
        assert thing_id is not None
        assert isinstance(thing_id, str)

    def test_thing_bulk_creation(self, app, random_name):
        names = [random_name() for i in range(self.BULK_CREATION_NUMBER)]
        things = app.api.create_things_bulk(names)
        assert isinstance(things, list)
        created_names = [t['name'] for t in things]
        for name in names:
            assert name in created_names

    def test_delete_thing(self, app, random_name):
        thing_name = random_name()
        _id = app.api.create_thing(thing_name)
        status_code = app.api.delete_thing(_id)
        assert status_code == 204

    def test_get_things(self, app, random_name):
        names = [random_name() for i in range(self.BULK_CREATION_NUMBER)]
        app.api.create_things_bulk(names)
        things = app.api.get_things()
        assert isinstance(things, list)
        assert len(things) == self.BULK_CREATION_NUMBER
        assert set([t['name'] for t in things]) == set(names)

    def test_get_thing(self, app, random_name):
        name = random_name()
        _id = app.api.create_thing(name)
        thing = app.api.get_thing(_id)
        assert isinstance(thing, dict)
        assert thing['id'] == _id
        assert thing['name'] == name


@pytest.mark.usefixtures('clean_things')
@pytest.mark.usefixtures('clean_channels')
class TestChannelsApi:
    BULK_CREATION_NUMBER = 5

    def test_create_channel(self, app, random_name):
        name = random_name()
        channel_id = app.api.create_channel(name)
        assert isinstance(channel_id, str)
        assert channel_id != ""
        channel_dict = app.api.get_channel(channel_id)
        assert channel_dict["id"] == channel_id
        assert channel_dict["name"] == name

    def test_delete_all_channels(self, app):
        channels_names = [str(i) for i in range(self.BULK_CREATION_NUMBER)]
        channels = app.api.create_channels_bulk(channels_names)
        assert len(channels) == len(channels_names)
        app.api.delete_all_channels()
        channels = app.api.get_channels()
        assert channels == []

    def test_delete_channel(self, app, random_name):
        name = random_name()
        channel_id = app.api.create_channel(name)
        status_code = app.api.delete_channel(channel_id)
        assert isinstance(status_code, int)
        assert status_code == 204
        channel_dict = app.api.get_channel(channel_id)
        assert channel_dict["error"] == "non-existent entity"

    def test_connect_thing_to_channel(self, app, random_name):
        channel_name = random_name()
        thing_name = random_name()

        channel_id = app.api.create_channel(channel_name)
        thing_id = app.api.create_thing(thing_name)
        status_code = app.api.connect_thing_to_channel(thing_id, channel_id)

        assert isinstance(status_code, int)
        assert status_code == 200

    def test_get_connected_things(self, app, random_name):
        things_number = 3

        channel_name = random_name()
        channel_id = app.api.create_channel(channel_name)

        thing_ids = []
        thing_names = []
        for i in range(things_number):
            name = random_name()
            thing_id = app.api.create_thing(name)
            app.api.connect_thing_to_channel(thing_id, channel_id)
            thing_ids.append(thing_id)
            thing_names.append(name)

        things = app.api.get_connected_things(channel_id)
        assert isinstance(things, list)
        assert len(things) == things_number
        for th in things:
            assert isinstance(th, dict)
            assert th["id"] in thing_ids
            assert th["name"] in thing_names

    def test_disconnect_thing_from_channel(self, app, random_name):
        channel_name = random_name()
        thing_name = random_name()

        channel_id = app.api.create_channel(channel_name)
        thing_id = app.api.create_thing(thing_name)

        app.api.connect_thing_to_channel(thing_id, channel_id)

        status_code = app.api.disconnect_thing_from_channel(channel_id, thing_id)
        assert isinstance(status_code, int)
        assert status_code == 204
        channel_things = app.api.get_connected_things(channel_id)
        for th in channel_things:
            assert thing_id != th["id"]
