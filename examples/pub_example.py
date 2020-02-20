from mainflux.app import MainfluxApp
from mainflux.thing import Thing
from mainflux.message import RandomMessage


MAINFLUX_IP = "ip_or_domain_of_your_mainflux"
MAINFLUX_PORT = "80"
USER_EMAIL = "user@example.com"
USER_PASSWORD = "some-password"


app = MainfluxApp(url=MAINFLUX_IP,
                  port=MAINFLUX_PORT,
                  user_email=USER_EMAIL,
                  user_password=USER_PASSWORD)


pub_thing = Thing(app)
print(pub_thing)

for i in range(10):
    pub_thing.send_message(RandomMessage(f"test_message_{i}"))


if __name__ == '__main__':
    app.run()
