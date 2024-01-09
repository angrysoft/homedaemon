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

    // @SuppressWarnings("unchecked")
    // private void onMessage(String topic, String msg) {
    // Gson gson = new
    // GsonBuilder().setObjectToNumberStrategy(ToNumberPolicy.LONG_OR_DOUBLE).create();
    // Type mapType = new TypeToken<HashMap<String, Object>>() {
    // }.getType();
    // HashMap<String, Object> notify = (HashMap<String, Object>) gson.fromJson(msg, mapType);
    // notify.forEach((k, v) -> {
    // if (v == null)
    // return;
    // String name = getStatusName(k);
    // Object value = v;
    // if (v instanceof Number) {
    // value = ((Number)v).intValue();
    // }

    // if (v instanceof String) {
    // value = ((String)v).toLowerCase();
    // }
    // handler.call(Event.statusEvent(getSidFromTopic(topic), name, value));
    // });
    // }

    void onMessage(String topic, String data) {
        JsonObject ewelinkNotify = json.fromJson(data, JsonObject.class);
        for (Entry<String, JsonElement> entry : ewelinkNotify.entrySet()) {
            Object value = null;
            JsonElement element = entry.getValue();
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
