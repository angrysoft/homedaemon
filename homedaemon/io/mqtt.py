import json
from homedaemon.io import BaseInput
from homedaemon.bus import Bus
from typing import Any, Dict
import paho.mqtt.client as mqtt


class Input(BaseInput):
    def __init__(self, bus: Bus, config: Dict[str, Any], loop):
        super(Input, self).__init__(bus, loop)
        self.config: Dict[str, str] = config.get("mqtt", {})
        self._client: mqtt.Client = mqtt.Client()
        self._client.on_connect: Callable[[...], None] = self._on_connect
        self._client.on_disconnect = self._on_disconnet
        if {"user", "password"}.issubset(self.config.keys()):
            self._client.username_pw_set(username=user, password=password)
        self._client.connect(host=host, port=port, keepalive=60)

    def _on_connect(
        self, client: mqtt.Client, userdata: Any, flags: Any, rc: Any
    ) -> None:
        self._connected = True
        to_subscribe: Set[str] = self._topics.copy()
        for topic in to_subscribe:
            client.subscribe(topic)

    def _on_disconnet(self, client: mqtt.Client, userdata: Any, rc: Any):
        self._connected = False
        if rc != 0:
            client.reconnect()

    def send(self, device_id: str, payload: Dict[str, Any]) -> None:
        self._client.publish(f"zigbee2mqtt/{device_id}/set", json.dumps(payload))

    def run(self):
        return super().run()
