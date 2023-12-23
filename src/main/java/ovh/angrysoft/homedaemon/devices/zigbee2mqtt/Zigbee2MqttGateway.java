package ovh.angrysoft.homedaemon.devices.zigbee2mqtt;

import java.util.Map;
import java.util.function.BiConsumer;
import java.util.logging.Level;

import org.eclipse.paho.mqttv5.common.MqttException;

import ovh.angrysoft.homedaemon.connections.MqttV5Connection;
import ovh.angrysoft.homedaemon.connections.MqttV5Connection.Builder;
import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.watcher.Zigbee2MqttWatcher;

public class Zigbee2MqttGateway extends BaseDevice implements Gateway {
    private MqttV5Connection connection;

    public Zigbee2MqttGateway(DeviceInfo devInfo) {
        super(devInfo);
        Builder connBuilder = MqttV5Connection.builder();
        Map<String, String> args = devInfo.getArgs();
        connBuilder.uri(args.get("uri"));
        if (args.containsKey("user"))
            connBuilder.user(args.get("user"));
        if (args.containsKey("password"))
            connBuilder.password(args.get("password"));
        this.connection = connBuilder.build();
        this.connection.start();
    }

    public void sendSet(String sid, String cmd, Object value) {
        String topic = String.format("zigbee2mqtt/%s/set", sid);
        String msg = String.format("{\"%s\": \"%s\"}", cmd, value);
        this.send(msg, topic);
    }

    public void sendGet(String sid, String cmd, Object value) {
        String topic = String.format("zigbee2mqtt/%s/get", sid);
        String msg = String.format("{\"%s\": \"%s\"}", cmd, value);
        this.send(msg, topic);
    }

    public void send(String msg, String topic) {
        try {
            this.connection.publishMessage(msg.getBytes(), 0, false, topic);
        } catch (MqttException e) {
            logger.log(Level.SEVERE, "Zigbee2mqtt gateway : {0}", e.getMessage());
        }

    }

    public void setOnMsgHandler(BiConsumer<String, String> handler) {
        this.connection.setOnMsgHandler(handler);
    }

    public void registerSubDevice(String sid, String model) {
        this.connection.addTopic(String.format("zigbee2mqtt/%s", sid));
    }

    @Override
    public void setup() {
        this.watcher = new Zigbee2MqttWatcher(this);
    }
}
