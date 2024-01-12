package ovh.angrysoft.homedaemon.watcher;

import java.util.Map.Entry;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.devices.zigbee2mqtt.Zigbee2MqttGateway;

public class Zigbee2MqttWatcher extends Watcher {
    private Zigbee2MqttGateway gateway;
    private Gson json = new Gson();

    public Zigbee2MqttWatcher(Zigbee2MqttGateway gateway) {
        super("Zigbee2Mqtt");
        this.gateway = gateway;
        this.gateway.setOnMsgHandler(this::onMessage);

    }

    void onMessage(String topic, String data) {
        JsonObject ewelinkNotify = json.fromJson(data, JsonObject.class);
        for (Entry<String, JsonElement> entry : ewelinkNotify.entrySet()) {
            JsonElement element = entry.getValue();
            if (element.isJsonNull())
                continue;
            Object value = null;
            String key = entry.getKey();
            String name = key;
            switch (key) {
                case "state_left":
                    name = "outlet0";
                    value = element.getAsString().toLowerCase();
                    break;
                case "state_center":
                    name = "outlet1";
                    value = element.getAsString().toLowerCase();
                    break;
                case "state_right":
                    if (ewelinkNotify.get("state_center") != null)
                        name = "outlet2";
                    else
                        name = "outlet1";
                    value = element.getAsString().toLowerCase();
                    break;
                case "state_l1":
                case "state_l2":
                case "state_l3":
                case "state_l4":
                case "state_l5":
                case "state_l6":
                case "state_l7":
                case "state_l8":
                case "state_l9":
                case "state_l10":
                    name = key.replace("state_l", "outlet");
                    value = element.getAsString().toLowerCase();
                    break;
                case "state":
                    value = element.getAsString().toLowerCase();
                    break;

                case "occupancy":
                case "contact":
                    value = element.getAsBoolean();
                    break;

                case "illuminance":
                case "illuminance_lux":
                case "humidity":
                case "temperature":
                case "pressure":
                    value = element.getAsInt();
                    break;

                default:
                    value = element.getAsString();
            }
            handler.call(Event.statusEvent(getSidFromTopic(topic), name, value));
        }
    }

    private String getSidFromTopic(String topic) {
        return topic.split("/")[1];
    }

    @Override
    public void run() {}

}
