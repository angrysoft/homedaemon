package ovh.angrysoft.homedaemon.io.mqtt;

import java.util.logging.Level;

import org.eclipse.paho.mqttv5.common.MqttException;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.ToNumberPolicy;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Topic;
import ovh.angrysoft.homedaemon.bus.Trigger;
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
                .autoReconnect(true)
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

    private void onMessage(String topic, String msg) {
        
        Gson gson = new GsonBuilder().setObjectToNumberStrategy(ToNumberPolicy.LONG_OR_DOUBLE).create();
        Msg notify = gson.fromJson(msg, Msg.class);

        Object value = notify.payload().value();
        if (value instanceof Long) {
            value = Integer.parseInt(value.toString());
        }
        bus.dispatch(Event.customEvent(notify.event(), notify.sid(), notify.payload().name() , value));
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

record Payload(String name, Object value) {
}

record Msg(String event, String sid, Payload payload) {
}