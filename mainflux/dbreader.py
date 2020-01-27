# imports

# [   #channels
#     {   #things
#         {   #thing
#             {
#                 "offset",
#                 #messages
#                 [
#
#                 ]
#             }
#         }
#     }
# ]

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
        # Old code
        """url = "{}/channels/{}/messages".format(DB_READER_URL, channel_id)
        headers = {"Authorization": thing_key}
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        try:
            return response.json()
        except Exception as e:
            print("Error:\n{}".format(e))
            return
        pass"""

    def _get_all_messages(self, offset=0, limit=LIMIT):
        # TODO Implement in accordance with new API
        """
        Gets all messages
        :param offset:
        :param limit:
        :return:
        """
        # Old code
        """for ch in self._things:
            ch_name = ch
            ch_id = self._things[ch]['channel'].get_id()
            self._messages.append({"channel":self._things[ch]['channel'], "things":{}})
            for th in self._things[ch]['things']:
                th_name = th.get_name()
                th_key = th.get_key()
                self._messages[-1]['things'][th_name] = {"thing":th, "messages":[]}
                th_offset = offset
                msgs = self._get_messages(ch_id, th_key, offset=th_offset, limit=limit)
                if msgs['messages']:
                    self._messages[-1]['things'][th_name]['messages'].extend(self._parse_message(msgs['messages']))
                total_msgs = msgs['total']
                th_offset += limit
                while th_offset < total_msgs:
                    msgs = self._get_messages(ch_id, th_key, offset=th_offset, limit=limit)
                    if msgs['messages']:
                        self._messages[-1]['things'][th_name]['messages'].extend(self._parse_message(msgs['messages']))
                    th_offset += limit"""

    def _parse_message(self, msg):
        # TODO Implement in accordance with new API
        """
        Parse one message and return Message instance
        :param msg:
        :return:
        """
        # Old code
        """if type(msg) is dict:
            name=None
            unit=None
            value=None
            sum=None
            time=0
            if 'channel' in msg:
                channel = msg['channel']
            if 'protocol' in msg:
                protocol = msg['protocol']
            if 'publisher' in msg:
                publisher = msg['publisher']
            if 'name' in msg:
                name = msg['name']
            if 'unit' in msg:
                unit = msg['unit']
            if 'value' in msg:
                value = msg['value']
            if 'sum' in msg:
                sum = msg['sum']
            if 'time' in msg:
                time = msg['time']
            return Message(channel, publisher, protocol, name=name, unit=unit,
                            value=value, sum=sum, time=time)
        if type(msg) is list:
            msg_list = []
            for entry in msg:
                msg_list.append(self._parse_message(entry))
            return msg_list
        return"""

    def get_thing_messages(self, thing):
        # TODO Implement in accordance with new API
        """
        Gets messages from one thing
        :param thing: Thing instance
        :return:
        """
        # Old code
        """th_key = thing.get_key()
        connected_channels = thing.get_connected_channels()
        th_msg = []
        if connected_channels:
            for ch in connected_channels:
                ch_id = ch['id']
                resp = self._get_messages(ch_id, th_key)
                total_msgs = resp['total']
                th_msg = resp['messages']
                if not th_msg:
                    return []
                offset = LIMIT
                if total_msgs > LIMIT:
                    while offset < total_msgs:
                        th_msg += self._get_messages(ch_id, th_key, offset=offset)['messages']
                        offset += LIMIT
                th_msg = [message for message in th_msg if message["publisher"] == thing.get_id()]
        return th_msg"""

    def get_channel_messages(self, channel):
        # TODO Implement in accordance with new API
        """
        Gets all messages in provided channel
        :param channel: Channel instance
        :return:
        """
        # Old code
        """ch_id = channel.get_id()
        connected_things = channel.get_things()
        channel_messages = []
        if connected_things:
            th_key = connected_things[0]['key']
            resp = self._get_messages(ch_id, th_key)
            total_msgs = resp['total']
            channel_messages = resp['messages']
            if total_msgs > 10:
                channel_messages += self._get_messages(ch_id, th_key, offset=10, limit=total_msgs)['messages']
        return channel_messages"""
