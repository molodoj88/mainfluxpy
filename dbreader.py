from settings import *
import requests
from channel import Channel
from thing import Thing
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

class DBReader:
    def __init__(self, user_token):
        self._token = user_token
        self._channels = []
        self._things = {}
        self._messages = []
        self._get_channels()
        self._get_things()
        self._get_all_messages(limit=5)
        pprint(self._messages)
        pprint(self._channels)
        pprint(self._things)

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
                self._things[ch_name]['things'].append(Thing(th['id'], th['name'], th['key'], self._token))

    def _get_messages(self, channel_id, thing_key, offset=0, limit=10):
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

    def _get_all_messages(self, offset=0, limit=10):
        for ch in self._things:
            ch_name = ch
            ch_id = self._things[ch]['channel'].get_id()
            self._messages.append({"channel":self._things[ch]['channel'], "things":{}})
            for th in self._things[ch]['things']:
                th_name = th.get_name()
                print(th_name)
                th_key = th.get_key()
                self._messages[-1]['things'][th_name] = {"thing":th, "messages":[]}
                th_offset = offset
                msgs = self._get_messages(ch_id, th_key, offset=th_offset, limit=limit)
                self._messages[-1]['things'][th_name]['messages'].extend(msgs['messages'])
                total_msgs = msgs['total']
                th_offset += limit
                while th_offset < total_msgs:
                    msgs = self._get_messages(ch_id, th_key, offset=th_offset, limit=limit)
                    self._messages[-1]['things'][th_name]['messages'].extend(msgs['messages'])
                    th_offset += limit
        pass
