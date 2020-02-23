from mainflux.app import MainfluxApp
from mainflux.thing import Thing
from mainflux.message import RandomMessage
import asyncio


MAINFLUX_IP = "10.10.3.107"
MAINFLUX_PORT = "80"
# USER_EMAIL = "komrad.alexey-pas2012@yandex.ru"
USER_PASSWORD = "12345678"

THING_ID = "69652021-e541-4871-8724-c49daa392a89"


app = MainfluxApp(url=MAINFLUX_IP,
                  port=MAINFLUX_PORT,
                  # user_email=USER_EMAIL,
                  user_password=USER_PASSWORD)


pub_thing = app.things_repository.get_thing(THING_ID)
print(pub_thing)
pub_thing.start_publishing()


async def signal_handler(thing, loop):
    while True:
        message = await loop.run_in_executor(None, input, "Input message to send:\n")
        if message:
            thing.send_message(RandomMessage(message))


if __name__ == '__main__':
    app.add_signal_handler(signal_handler, THING_ID)
    app.run()
