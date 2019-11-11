import threading
from thing import ThingsFactory
from message import RandomMessage
from random import choice, random
from main import get_all_things, get_token
from queue import Queue
from time import sleep
from dbreader import DBReader
from paho.mqtt.client import error_string
import paho.mqtt.client as paho
from pprint import pprint


MESSAGES_BY_THING = 10
RANDOM_CHANNEL = False


def _test(_things, event, counter):
    _thing = _things.get()
    if _things.empty():
        event.set()
    name = _thing.get_id()
    connected_channels = _thing.get_connected_channels()
    channel_id = connected_channels[0]["id"]
    if RANDOM_CHANNEL:
        pass
    for i in range(1, MESSAGES_BY_THING + 1):
        message = RandomMessage(name)
        result = _thing.send_message(message.get_json(), channel_id)
        # print("send message {} from thing {} to channel {}".format(i, _thing.get_id(), channel_id))
        counter["all"] += 1
        if result.rc != paho.MQTT_ERR_SUCCESS:
            counter["errors"] += 1
            print("Thing {}, message n. {}, error: {}".format(name, i, error_string(result.rc)))
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
            things_queue = Queue()
            counter = {"all": 0, "errors": 0}
            stop_event = threading.Event()
            for t in ThingsFactory.things:
                connected_channels = t.get_connected_channels()
                if not connected_channels:
                    continue
                things_queue.put(t)
                connected_things.append(t)
            for t in connected_things:
                thing_id = t.get_id()
                summary[thing_id] = {}
                summary[thing_id]["before"] = reader.get_thing_msg_count(t)
            print("Start process ({} messages by thing)".format(MESSAGES_BY_THING))
            while True:
                try:
                    if stop_event.is_set():
                        break
                    process = threading.Thread(target=_test, args=(things_queue, stop_event, counter))
                    all_processes.append(process)
                    process.start()
                    print("Process #{} started".format(len(all_processes)))
                    sleep(1)
                except KeyboardInterrupt:
                    break

            for proc in all_processes:
                proc.join()

            sleep(3)

            for t in connected_things:
                thing_id = t.get_id()
                after = reader.get_thing_msg_count(t)
                before = summary[thing_id]["before"]
                summary[thing_id]["after"] = after
                summary[thing_id]["success"] = (after - before) / MESSAGES_BY_THING

            print("\nSummary:\n")
            pprint(summary)
