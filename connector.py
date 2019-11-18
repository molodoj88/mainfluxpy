# imports
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2


class Connector:
    def __init__(self, url, port):
        self._url = url
        self._port = port


class MqttConnector(Connector):
    def __init__(self, url, username, password, port=1883):
        super().__init__(url, port)
        self._username = username
        self._password = password
        self.mqtt_client = MQTTClient()
        self.mqtt_client.connect("mqtt://{}:{}@{}:{}/".format(self._username, self._password, self._url, self._port))

    def send_message(self, message, topic):
        self.mqtt_client.publish(topic, message, qos=QOS_1)

    def disconnect(self):
        self.mqtt_client.disconnect()
