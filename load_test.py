import threading
from thing import ThingsFactory
from message import RandomMessage
from random import choice, random
from main import get_all_things, get_token
from queue import Queue
from time import sleep
from dbreader import DBReader
from pprint import pprint
import asyncio


MESSAGES_BY_THING = 10
RANDOM_CHANNEL = False


async def _test(_thing, counter):
    name = _thing.get_id()
    connected_channels = _thing.get_connected_channels()
    channel_id = connected_channels[0]["id"]
    if RANDOM_CHANNEL:
        pass
    for i in range(1, MESSAGES_BY_THING + 1):
        message = RandomMessage(name)
        result = await _thing.send_message(message.get_json(), channel_id)
        print("send message {} from thing {} to channel {}".format(i, _thing.get_id(), channel_id))
        counter["all"] += 1
        if not result:
            counter["errors"] += 1
            print("Thing {}, message n. {}, !!!error!!!".format(name, i))
        sleep(random())


if __name__ == "__main__":
    token = get_token()
    reader = DBReader(token)
    summary = {}
    all_processes = []
    if token:
        print(token)
        _things = get_all_things(token)
        for t in _things:
            ThingsFactory.get_thing(t["id"], t["name"], t["key"], token)
        if ThingsFactory.things:
            connected_things = []
            counter = {"all": 0, "errors": 0}
            for t in ThingsFactory.things:
                connected_channels = t.get_connected_channels()
                if not connected_channels:
                    continue
                connected_things.append(t)
            for t in connected_things:
                thing_id = t.get_id()
                summary[thing_id] = {}
                summary[thing_id]["before"] = reader.get_thing_msg_count(t)

            for t in connected_things:
                thing_id = t.get_id()
                after = reader.get_thing_msg_count(t)
                before = summary[thing_id]["before"]
                summary[thing_id]["after"] = after
                summary[thing_id]["success"] = (after - before) / MESSAGES_BY_THING

            print("\nSummary:\n")
            pprint(summary)
