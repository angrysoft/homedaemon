package ovh.angrysoft.homedaemon.devices.zigbee2mqtt;

import java.util.function.BiConsumer;
import java.util.logging.Level;

import org.eclipse.paho.mqttv5.common.MqttException;

import ovh.angrysoft.homedaemon.connections.MqttV5Connection;
import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;

public class Zigbee2MqttGateway extends BaseDevice implements Gateway {
    private MqttV5Connection connection;

    public Zigbee2MqttGateway(DeviceInfo devInfo) {
        if (devInfo.getArgs() != null)
            this.connection = new MqttV5Connection(devInfo.getArgs());
        this.connection.connect();
    }

    public void send(String sid, String msg) {
        String topic = String.format("zigbee2mqtt/%s/set", sid);
        try {
            this.connection.publishMessage(msg.getBytes(), 0, false, topic);
        } catch (MqttException e) {
            LOGGER.log(Level.SEVERE, "Zigbee2mqtt gateway : {0}", e.getMessage());
            ;
        }
    }

    public void setOnMsgHandler(BiConsumer<String, String> handler) {
        this.connection.setOnMsgHandler(handler);
    }

    public void registerSubDevice(String sid, String model) {
        this.connection.addTopic(String.format("zigbee2mqtt/%s", sid));
    }

}
