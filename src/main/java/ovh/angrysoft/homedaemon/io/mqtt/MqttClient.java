package ovh.angrysoft.homedaemon.io.mqtt;

import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.logging.Level;

import org.eclipse.paho.mqttv5.common.MqttException;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.ToNumberPolicy;
import com.google.gson.reflect.TypeToken;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Topic;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.bus.Events.ExecuteEvent;
import ovh.angrysoft.homedaemon.config.Config;
import ovh.angrysoft.homedaemon.config.ConfigType;
import ovh.angrysoft.homedaemon.config.HomedConfig;
import ovh.angrysoft.homedaemon.connections.MqttV5Connection;
import ovh.angrysoft.homedaemon.io.BaseIo;

public class MqttClient extends BaseIo {
    private MqttV5Connection connection;
    private String homeId;

    public MqttClient(Config config, EventBus bus) {
        super(config, bus);
        this.config.resisterConfigType("mqttClient", new ConfigType<>(MqttClientConfig.class));
        MqttClientConfig mqttConfig = (MqttClientConfig) this.config.get("mqttClient");
        HomedConfig homedConfig = (HomedConfig) this.config.get("homed");
        this.homeId = homedConfig.id();

        this.connection = MqttV5Connection.builder()
                .uri(mqttConfig.uri())
                .user(mqttConfig.user())
                .password(mqttConfig.password())
                .build();

        this.connection.addTopic(new StringBuilder("homed/")
                .append(homeId)
                .append("/set")
                .toString());
        this.connection.setOnMsgHandler((String topic, String msg) -> {
            onMessage(topic, msg);
        });

        bus.addTrigger(new Trigger(Topic.fromString("status.*"), (Event event) -> {
            this.sendEvent(event);
        }));
    }

    @SuppressWarnings("unchecked")
    private void onMessage(String topic, String msg) {
        Gson gson = new GsonBuilder().setObjectToNumberStrategy(ToNumberPolicy.LONG_OR_DOUBLE).create();
        Type mapType = new TypeToken<HashMap<String, Object>>() {
        }.getType();

        HashMap<String, Object> notify = (HashMap<String, Object>) gson.fromJson(msg, mapType);
        notify.forEach((k, v) -> {
            Object value = v;
            if (v instanceof Long) {
                value = Integer.parseInt(v.toString());
            }
            bus.dispatch(new ExecuteEvent(topic.split("/")[1], k, value));
        });
    }

    private void sendEvent(Event event) {
        String topic = new StringBuilder("homed/")
                .append(homeId)
                .append("/get")
                .toString();
    
        try {
            this.connection.publishMessage(event.toJson().getBytes(), 0, false, topic);
        } catch (MqttException e) {
            LOGGER.log(Level.SEVERE, "Mqtt client : {0}", e.getMessage());
        }
    }

    @Override
    public void run() {
        this.connection.start();
    }

}
