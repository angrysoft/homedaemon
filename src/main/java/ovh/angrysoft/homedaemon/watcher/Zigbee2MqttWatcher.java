package ovh.angrysoft.homedaemon.watcher;

import java.util.HashMap;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.ToNumberPolicy;
import com.google.gson.ToNumberStrategy;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.devices.zigbee2mqtt.Zigbee2MqttGateway;

public class Zigbee2MqttWatcher extends Watcher {
    private Zigbee2MqttGateway gateway;

    public Zigbee2MqttWatcher(Zigbee2MqttGateway gateway) {
        super("Zigbee2Mqtt");
        this.gateway = gateway;
        this.gateway.setOnMsgHandler((String topic, String msg) -> {
            onMessage(topic, msg);
        });
        
    }
    
    @SuppressWarnings("unchecked")
    private void onMessage(String topic, String msg) {
        Gson gson = new GsonBuilder().setObjectToNumberStrategy(ToNumberPolicy.LONG_OR_DOUBLE).create();
        HashMap<String, Object> notify = (HashMap<String, Object>) gson.fromJson(msg, HashMap.class);
        notify.forEach((k, v) -> {
            handler.call(new StatusEvent(getSidFromTopic(topic), k, v));
        });
    }
    
    private String getSidFromTopic(String topic) {
        return topic.split("/")[1];
    }
    
    @Override
    public void run() {
    }

}
