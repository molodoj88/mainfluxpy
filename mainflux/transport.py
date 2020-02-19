from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2
from .message import Message
from typing import Callable
import asyncio

MQTT = "mqtt"
HTTP = "http"
COAP = "coap"


class TransportException(Exception):
    pass


class NotSupportedTransportError(TransportException):
    pass


class TransportFactory:

    def __init__(self, transport):
        self.transport = transport

    @staticmethod
    def _create_mqtt_transport(channel, port: int = None):
        url = channel.app.ip
        app = channel.app
        username = channel.thing.thing_id
        password = channel.thing.key
        return MqttTransport(app, url, username, password, port)

    @staticmethod
    def _create_http_transport(channel, port: int = None):
        pass

    @staticmethod
    def _create_coap_transport(channel, port: int = None):
        pass

    def create_transport(self, channel, port: int = None):
        """
        Creates transport for channel based on app.config.TRANSPORT
        :param channel: channel object
        :param port: port for connection
        :return:
        """
        if self.transport == MQTT:
            return self._create_mqtt_transport(channel, port)
        elif self.transport == HTTP:
            return self._create_http_transport(channel, port)
        elif self.transport == COAP:
            return self._create_coap_transport(channel, port)
        else:
            raise NotSupportedTransportError(f"Transport '{self.transport}' is not supported")


class AbstractTransport:
    def __init__(self, app, url, port):
        self._app = app
        self._url = url
        self._port = port

    def send_message(self, message, topic):
        raise NotImplementedError

    async def subscribe(self, topic: str, message_received_cb=None):
        raise NotImplementedError

    async def connect(self):
        raise NotImplementedError

    async def disconnect(self):
        raise NotImplementedError


class MqttTransport(AbstractTransport):
    def __init__(self, app, url: str, username: str, password: str, port: int):
        port = port or 1883
        super().__init__(app, url, port)
        self._username = username
        self._password = password
        self.address = "mqtt://{}:{}@{}:{}/".format(self._username,
                                                    self._password,
                                                    self._url,
                                                    self._port)
        self.mqtt_client = MQTTClient()
        self.connected = False
        self._message_received_cb = None

    async def _send_message(self, message: Message, topic: str):
        result = None
        message = message.as_json().encode('utf-8')
        try:
            result = await self.mqtt_client.publish(topic, message, qos=QOS_1)
        except ConnectException as ce:
            print("Connection failed: %s" % ce)
        return result

    async def send_message(self, message: Message, topic: str):
        """
        Sends message to a topic
        :param message: message.Message instance
        :param topic: topic
        :return:
        """
        if not self.connected:
            await self.connect()
        await self._send_message(message, topic)

    async def _connect(self):
        try:
            await self.mqtt_client.connect(self.address)
        except ConnectException:
            print("Can't connect to mqtt broker on address: %s" % self.address)

    async def connect(self):
        """
        Connects to a broker
        :return:
        """
        while not self.connected:
            await self._connect()
            print("Connected to mqtt broker on address %s" % self.address)
            self.connected = True

    async def _disconnect(self):
        await self.mqtt_client.disconnect()

    async def disconnect(self):
        if self.connected:
            await self._disconnect()
            self.connected = False
            print("Disconnected from mqtt broker on address %s" % self.address)

    def message_received_callback(self, message):
        if self._message_received_cb:
            return self._message_received_cb(message)
        else:
            print(message)

    async def _subscribe(self, topic: str):
        """
        Subscribes to provided topic and waits for messages async.
        If callback function were provided
        :param topic: topic
        :return:
        """
        try:
            topics = [(topic, QOS_0)]
            await self.mqtt_client.subscribe(topics)
            while True:
                if not self.connected:
                    break
                message = await self.mqtt_client.deliver_message()
                self.message_received_callback(message)
        except ConnectException as ce:
            print("Connection failed: %s" % ce)

    async def subscribe(self, topic: str, message_received_cb: Callable):
        """
        Subscribes to sub channel over mqtt and
        sets callback for received message
        :param topic: topic to subscribe
        :param message_received_cb: callback for received message (first argument should be message: str)
        :return:
        """
        if message_received_cb is not None:
            self._message_received_cb = message_received_cb
        while not self.connected:
            await asyncio.sleep(0.01)
        await self._subscribe(topic)
