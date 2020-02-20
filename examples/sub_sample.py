from mainflux.app import MainfluxApp
from mainflux.thing import Thing


MAINFLUX_IP = "ip_or_domain_of_your_mainflux"
MAINFLUX_PORT = "80"
USER_EMAIL = "user@example.com"
USER_PASSWORD = "some-password"


app = MainfluxApp(url=MAINFLUX_IP,
                  port=MAINFLUX_PORT,
                  user_email=USER_EMAIL,
                  user_password=USER_PASSWORD)

sub_thing = Thing(app)
print(sub_thing)
sub_thing.subscribe()


if __name__ == '__main__':
    app.run()
