from settings import *
import requests
from channel import Channel
from thing import Thing


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


def main():
    token = get_token()
    if token:
        channels = get_channels(token)
        if channels:
            first_channel = channels[0]
            channel_id = first_channel["id"]
            channel_name = first_channel["name"]
            channel = Channel(channel_id, channel_name, token)
            _things = channel.get_things()
            if _things:
                things_params = [(t["id"], t["name"], t["key"]) for t in _things]
                things = [Thing(_id, _name, _key, token) for _id, _name, _key in things_params]
                for t in things:
                    print(t.get_connected_channels())
                    t.send_message("some message", channel.get_id())


if __name__ == "__main__":
    main()
