from settings import *
import requests
from channel import Channel
from thing import Thing
from message import Message, RandomMessage


def get_token():
    url = "{}/tokens".format(MAINFLUX_URL)
    headers = {"Content-Type": "application/json"}
    data = {"email": MAINFLUX_USER_EMAIL, "password": MAINFLUX_USER_PASSWORD}
    response = requests.post(url, headers=headers, json=data)
    try:
        token = response.json()["token"]
    except Exception as e:
        print("Error:\n{}".format(e))
        return
    return token


def get_channels(token):
    url = "{}/channels".format(MAINFLUX_URL)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    try:
        channels = response.json()["channels"]
    except Exception as e:
        print("Error:\n{}".format(e))
        return
    return channels


def get_all_things(token):
    # TODO Сделать получение всех устройств (если их больше 100)
    url = "{}/things".format(MAINFLUX_URL)
    headers = {"Authorization": token}
    params = {"limit": 100}
    response = requests.get(url, headers=headers, params=params)
    return response.json()["things"]


def main():
    token = get_token()
    if token:
        _things = get_all_things(token)
        if _things:
            things_params = [(t["id"], t["name"], t["key"]) for t in _things]
            things = [Thing(_id, _name, _key, token) for _id, _name, _key in things_params]
            for t in things:
                _channel = t.get_connected_channels()[0]
                channel = Channel(_channel["id"], _channel["name"], token)
                message = RandomMessage(name=t.get_name())
                print(message.get_json())
                t.send_message(message.get_json(), channel.get_id())


if __name__ == "__main__":
    main()
