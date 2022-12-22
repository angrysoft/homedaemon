import json
from homedaemon.io import BaseInput
from homedaemon.bus import Bus
from typing import Any, Dict
import paho.mqtt.client as mqtt
from time import sleep


class Input(BaseInput):
    def __init__(self, bus: Bus, config: Dict[str, Any], loop):
        super(Input, self).__init__(bus, loop)
        self.config: Dict[str, Any] = config
        self.devices = []
        self._connected = False
        self._client: mqtt.Client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_disconnect = self._on_disconnect
        if {"user", "password"}.issubset(self.config.get("mqtt", {}).keys()):
            self._client.username_pw_set(
                username=self.config["mqtt"]["user"],
                password=self.config["mqtt"]["password"],
            )
        self._client.tls_set()
        self._client.connect(
            host=self.config.get("mqtt", {}).get("host", "localhost"),
            port=self.config.get("mqtt", {}).get("port", 1883),
            keepalive=self.config.get("mqtt", {}).get("keepalive", 60),
        )
        self.bus.add_trigger("report.*.*.*", self.publish_msg)
        self.bus.add_trigger("homed.device.init.*", self.collect_init_devices)
        self.bus.add_trigger("info.homed.status.started", self.send_devices)

    def collect_init_devices(self, dev):
        self.devices.append(dev)

    def send_devices(self, *args):
        while not self._connected:
            sleep(0.5)
        for dev in self.devices:
            self.publish_msg(dev)

    def _on_connect(
        self, client: mqtt.Client, userdata: Any, flags: Any, rc: Any
    ) -> None:
        self._connected = True
        client.subscribe(f'homed/{self.config["homed"]["id"]}/set')

    def _on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
        try:
            _msg = json.loads(msg.payload)
            print(msg.payload, _msg)
            if event := _msg.get("event"):
                args = _msg.get("args")
                if args[1] is None:
                    self.bus.emit(event, (args[0],))
                else:
                    self.bus.emit(event, args)

        except json.JSONDecodeError as err:
            print(f"json {err} : {msg}")

    def _on_disconnect(self, client: mqtt.Client, userdata: Any, rc: Any):
        self._connected = False
        if rc != 0:
            client.reconnect()

    def publish_msg(self, payload: Dict[str, Any]) -> None:
        if self._connected:
            self._client.publish(
                f'homed/{self.config["homed"]["id"]}/get', json.dumps(payload), qos=1
            )

    def run(self):
        self._client.loop_forever()
