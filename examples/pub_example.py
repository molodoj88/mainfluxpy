from mainflux.app import MainfluxApp
from mainflux.message import RandomMessage


MAINFLUX_IP = "ip-or-domain-name"
MAINFLUX_PORT = "80"
USER_EMAIL = "your-username-at-mainflux"
USER_PASSWORD = "your-password-on-mainflux"
THING_ID = None  # Optionally, if you have existing thing at mainflux


app = MainfluxApp(url=MAINFLUX_IP,
                  port=MAINFLUX_PORT,
                  user_email=USER_EMAIL,
                  user_password=USER_PASSWORD)


pub_thing = app.things_repository.get_thing(THING_ID)
if THING_ID is None:
    THING_ID = pub_thing.thing_id
print(pub_thing)
pub_thing.start_publishing()


async def signal_handler(thing, loop):
    """
    In this handler we wait user input and send message from our pub_thing
    """
    while True:
        message = await loop.run_in_executor(None, input, "Input message to send:\n")
        if message:
            thing.send_message(RandomMessage(message))


if __name__ == '__main__':
    app.add_signal_handler(signal_handler, THING_ID)
    app.run()
