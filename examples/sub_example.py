from mainflux.app import MainfluxApp


MAINFLUX_IP = "ip-or-domain-name"
MAINFLUX_PORT = "80"
USER_EMAIL = "your-username-at-mainflux"
USER_PASSWORD = "your-password-on-mainflux"
THING_ID = None  # Optionally, if you have existing thing at mainflux


app = MainfluxApp(url=MAINFLUX_IP,
                  port=MAINFLUX_PORT,
                  user_email=USER_EMAIL,
                  user_password=USER_PASSWORD)

sub_thing = app.things_repository.get_thing(thing_id=THING_ID)
if THING_ID is None:
    THING_ID = sub_thing.thing_id
print(sub_thing)
sub_thing.subscribe()


if __name__ == '__main__':
    app.run()
