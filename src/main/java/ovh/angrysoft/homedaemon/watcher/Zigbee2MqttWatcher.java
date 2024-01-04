package ovh.angrysoft.homedaemon.watcher;

import java.lang.reflect.Type;
import java.util.HashMap;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.ToNumberPolicy;
import com.google.gson.reflect.TypeToken;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.devices.zigbee2mqtt.Zigbee2MqttGateway;

public class Zigbee2MqttWatcher extends Watcher {
    private Zigbee2MqttGateway gateway;

    public Zigbee2MqttWatcher(Zigbee2MqttGateway gateway) {
        super("Zigbee2Mqtt");
        this.gateway = gateway;
        this.gateway.setOnMsgHandler(this::onMessage);

    }

    @SuppressWarnings("unchecked")
    private void onMessage(String topic, String msg) {
        Gson gson = new GsonBuilder().setObjectToNumberStrategy(ToNumberPolicy.LONG_OR_DOUBLE).create();
        Type mapType = new TypeToken<HashMap<String, Object>>() {
        }.getType();
        HashMap<String, Object> notify = (HashMap<String, Object>) gson.fromJson(msg, mapType);
        notify.forEach((k, v) -> {
            if (v == null)
                return;
            Object value = v;
            if (v instanceof Number) {
                value = ((Number)v).intValue();
            }
            handler.call(Event.statusEvent(getSidFromTopic(topic), k, value));
        });
    }

    private String getSidFromTopic(String topic) {
        return topic.split("/")[1];
    }

    @Override
    public void run() {
    }

}
