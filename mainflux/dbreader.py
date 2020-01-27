# imports

LIMIT = 100


class DBReader:
    """
    Class for main database reader.
    Contains functions for getting messages stored in influx db,
    filtering them by channels and things.
    """
    # TODO Add app in __init__
    def __init__(self, user_token):
        self._token = user_token
        self._channels = []
        self._things = {}

    def _get_channels(self, offset=0, limit=LIMIT):
        # TODO Implement in accordance with new API
        """
        Gets all channels from mainflux database
        :param offset:
        :param limit:
        :return:
        """
        pass

    def _get_things(self):
        # TODO Implement in accordance with new API
        """
        Gets all things from mainflux database
        :return:
        """
        pass

    def _get_messages(self, channel_id, thing_key, offset=0, limit=LIMIT):
        # TODO Implement in accordance with new API
        """
        Gets messages from provided channel with provided thing key
        :param channel_id:
        :param thing_key:
        :param offset:
        :param limit:
        :return:
        """
        pass

    def _get_all_messages(self, offset=0, limit=LIMIT):
        # TODO Implement in accordance with new API
        """
        Gets all messages
        :param offset:
        :param limit:
        :return:
        """
        pass

    def _parse_message(self, msg):
        # TODO Implement in accordance with new API
        """
        Parse one message and return Message instance
        :param msg:
        :return:
        """
        pass

    def get_thing_messages(self, thing):
        # TODO Implement in accordance with new API
        """
        Gets messages from one thing
        :param thing: Thing instance
        :return:
        """
        pass

    def get_channel_messages(self, channel):
        # TODO Implement in accordance with new API
        """
        Gets all messages in provided channel
        :param channel: Channel instance
        :return:
        """
        pass
