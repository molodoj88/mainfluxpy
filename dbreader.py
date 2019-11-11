from settings import *
import requests
from channel import Channel
from thing import ThingsFactory
from message import Message
from pprint import pprint

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
    def __init__(self, user_token):
        self._token = user_token
        self._channels = []
        self._things = {}
        # self._messages = []
        # self._get_channels()
        # self._get_things()
        # self._get_all_messages(limit=5)

    def _get_channels(self, offset=0, limit=100):
        url = "{}/channels".format(MAINFLUX_URL)
        headers = {"Authorization": self._token}
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        try:
            channels = response.json()["channels"]
            self._channels = [Channel(ch['id'], ch['name'], self._token) for ch in channels]
        except Exception as e:
            print("Error:\n{}".format(e))
            return

    def _get_things(self):
        for ch in self._channels:
            ch_name = ch.get_name()
            things = ch.get_things()
            self._things[ch_name] = {"channel":ch, "things":[]}
            for th in things:
                self._things[ch_name]['things'].append(ThingsFactory.get_thing(th['id'],
                                                                               th['name'],
                                                                               th['key'],
                                                                               self._token))

    def _get_messages(self, channel_id, thing_key, offset=0, limit=LIMIT):
        url = "{}/channels/{}/messages".format(DB_READER_URL, channel_id)
        headers = { "Authorization": thing_key}
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        try:
            return response.json()
        except Exception as e:
            print("Error:\n{}".format(e))
            return
        pass

    def _get_all_messages(self, offset=0, limit=100):
        for ch in self._things:
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
                    th_offset += limit
        pass

    def _parse_message(self, msg):
        if type(msg) is dict:
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
        return

    def get_channels(self):
        return self._channels

    def get_things(self):
        return self._things

    def get_messages(self):
        return self._messages

    def get_thing_messages(self, thing):
        th_key = thing.get_key()
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
        return th_msg

    def get_channel_messages(self, channel):
        ch_id = channel.get_id()
        connected_things = channel.get_things()
        channel_messages = []
        if connected_things:
            th_key = connected_things[0]['key']
            resp = self._get_messages(ch_id, th_key)
            total_msgs = resp['total']
            channel_messages = resp['messages']
            if total_msgs > 10:
                channel_messages += self._get_messages(ch_id, th_key, offset=10, limit=total_msgs)['messages']
        return channel_messages

    def get_thing_summary(self, thing):
        msgs = self.get_thing_messages(thing)
        return {'thing_id': thing.get_id(), 'total messages': len(msgs)}

    def get_channel_summary(self, channel):
        msgs = self.get_channel_messages(channel)
        connected_things = channel.get_things()
        return {'things': len(connected_things), 'total messages': len(msgs)}

    def get_thing_msg_count(self, thing):
        return self.get_thing_summary(thing)['total messages']
