import threading
from thing import ThingsFactory
from message import RandomMessage
from random import choice, random
from main import get_all_things, get_token
from queue import Queue
from time import sleep
from dbreader import DBReader
from paho.mqtt.client import error_string


MESSAGES_BY_THING = 1
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
        message = RandomMessage(name)
        result = _thing.send_message(message.get_json(), channel_id)
        print("Message n.{} from thing `{}` has been sent. Result: {}".format(i, name, error_string(result.rc)))

        sleep(random())


if __name__ == "__main__":
    token = get_token()
    all_processes = []
    if token:
        _things = get_all_things(token)
        for t in _things:
            ThingsFactory.get_thing(t["id"], t["name"], t["key"], token)
        if ThingsFactory.things:
            queue = Queue()
            stop_event = threading.Event()
            for t in ThingsFactory.things:
                queue.put(t)
            while True:
                try:
                    if stop_event.is_set():
                        break
                    process = threading.Thread(target=_test, args=(queue, stop_event))
                    all_processes.append(process)
                    process.start()
                except KeyboardInterrupt:
                    break

            for proc in all_processes:
                proc.join()

            reader = DBReader(token)
            for t in ThingsFactory.things:
                if t.get_connected_channels():
                    print(reader.get_thing_summary(t))
