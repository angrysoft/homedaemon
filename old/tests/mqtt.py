import json
from typing import Any, Dict
import paho.mqtt.client as mqtt


def _on_connect(client: mqtt.Client, userdata: Any, flags: Any, rc: Any) -> None:
    print("Connected")
    client.subscribe("homed/aaaaaaaaaa/set")


def _on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    try:
        _msg = json.loads(msg.payload)
        if event := _msg.get("event"):
            args = _msg.get("args")
            print(args)
            if args[1] is None:
                print(event, (args[0],))
            else:
                print(event, args)

    except json.JSONDecodeError as err:
        print(f"json {err} : {msg}")


def _on_disconnect(_client: mqtt.Client, userdata: Any, rc: Any):
    if rc != 0:
        _client.reconnect()


def publish_msg(payload: Dict[str, Any]) -> None:
    print(
        "homed/aaaaaaaaaa/set",
        json.dumps(payload),
    )
    client.publish("homed/aaaaaaaaaa/set", json.dumps(payload))


with open("../tmp/conf.d/mqtt.json") as jfile:
    config = json.load(jfile)

print(config)

client: mqtt.Client = mqtt.Client()
client.on_connect = _on_connect
client.on_message = _on_message
client.on_disconnect = _on_disconnect
client.username_pw_set(
    username=config["user"],
    password=config["password"],
)
client.tls_set()
client.connect(
    host=config.get("host", "localhost"),
    port=config.get("port", 1883),
    keepalive=config.get("keepalive", 60),
)
print("before loop")

client.loop_forever()
