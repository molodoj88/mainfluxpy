import threading
from thing import Thing
from message import RandomMessage
from random import choice, random
from main import get_all_things, get_token
from queue import Queue
from time import sleep


MESSAGES_BY_THING = 10
RANDOM_CHANNEL = False


def _test(_things, event):
    _thing = _things.get()
    if _things.empty():
        event.set()
        return
    name = _thing.get_id()
    connected_channels = _thing.get_connected_channels()
    if not connected_channels:
        print("Thing {} is not connected to any channel".format(name))
        return
    channel_id = connected_channels[0]["id"]
    if RANDOM_CHANNEL:
        pass
    for i in range(1, MESSAGES_BY_THING + 1):
        print("Sending message n.{} from thing `{}`".format(i, name))
        message = RandomMessage(name)
        _thing.send_message(message.get_json(), channel_id)
        sleep(random())


if __name__ == "__main__":
    token = get_token()
    things = []
    if token:
        _things = get_all_things(token)
        things = [Thing(t["id"], t["name"], t["key"], token) for t in _things]
    if things:
        queue = Queue()
        stop_event = threading.Event()
        for t in things:
            queue.put(t)
        while True:
            try:
                if stop_event.is_set():
                    break
                process = threading.Thread(target=_test, args=(queue, stop_event))
                process.start()
            except KeyboardInterrupt:
                break
