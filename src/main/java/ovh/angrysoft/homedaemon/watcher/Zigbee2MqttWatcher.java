package ovh.angrysoft.homedaemon.watcher;

import java.util.HashMap;

import com.google.gson.Gson;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.devices.zigbee2mqtt.Zigbee2MqttGateway;

public class Zigbee2MqttWatcher extends Watcher {
    private Zigbee2MqttGateway gateway;

    public Zigbee2MqttWatcher(Zigbee2MqttGateway gateway) {
        super("Zigbee2Mqtt");
        this.gateway = gateway;
        this.gateway.setOnMsgHandler((String sid, String msg) -> {
            onMessage(sid, msg);
        });
    }

    @SuppressWarnings("unchecked")
    private void onMessage(String sid, String msg) {
        HashMap<String, Object> notify = (HashMap<String, Object>) new Gson().fromJson(msg, HashMap.class);
        notify.forEach((k, v) -> {
            handler.call(new StatusEvent(sid, k, v));
        });
    }

    @Override
    public void run() {
        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}
