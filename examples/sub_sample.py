from mainflux.app import MainfluxApp
from mainflux.thing import Thing


MAINFLUX_IP = "192.168.30.13"
MAINFLUX_PORT = "80"
USER_EMAIL = "komrad.alexey-pas2012@yandex.ru"
USER_PASSWORD = "123456"


app = MainfluxApp(url=MAINFLUX_IP,
                  port=MAINFLUX_PORT,
                  user_email=USER_EMAIL,
                  user_password=USER_PASSWORD)

sub_thing = Thing(app, "65f04770-946c-492e-a297-e42a08a2f158")
print(sub_thing)
sub_thing.subscribe()


if __name__ == '__main__':
    app.run()
