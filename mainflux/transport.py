# imports
from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2
import asyncio


class Transport:
    def __init__(self, url, port):
        self._url = url
        self._port = port

    def send_message(self, message, topic):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError


class MqttTransport(Transport):
    def __init__(self, url, username, password, port=1883):
        super().__init__(url, port)
        self._username = username
        self._password = password
        self.address = "mqtt://{}:{}@{}:{}/".format(self._username,
                                                    self._password,
                                                    self._url,
                                                    self._port)
        self.mqtt_client = MQTTClient()
        self.connected = False

    async def _send_message(self, message, topic):
        result = None
        message = message.encode('utf-8')
        try:
            result = await self.mqtt_client.publish(topic, message, qos=QOS_1)
        except ConnectException as ce:
            print("Connection failed: %s" % ce)
        return result

    def send_message(self, message, topic):
        if not self.connected:
            self.connect()
        asyncio.get_event_loop().run_until_complete(self._send_message(message, topic))

    async def _connect(self):
        try:
            await self.mqtt_client.connect(self.address)
        except ConnectException:
            print("Can't connect to mqtt broker on address: %s" % self.address)

    def connect(self):
        if not self.connected:
            asyncio.get_event_loop().run_until_complete(self._connect())
            print("Connected to mqtt broker on address %s" % self.address)
            self.connected = True

    async def _disconnect(self):
        await self.mqtt_client.disconnect()

    def disconnect(self):
        if self.connected:
            asyncio.get_event_loop().run_until_complete(self._disconnect())
            self.connected = False
            print("Disconnected from mqtt broker on address %s" % self.address)

    #def __del__(self):
    #    asyncio.get_event_loop().run_until_complete(self.disconnect())
