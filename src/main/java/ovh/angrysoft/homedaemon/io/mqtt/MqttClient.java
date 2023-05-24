package ovh.angrysoft.homedaemon.io.mqtt;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.config.Config;
import ovh.angrysoft.homedaemon.config.ConfigType;
import ovh.angrysoft.homedaemon.connections.MqttV5Connection;
import ovh.angrysoft.homedaemon.io.BaseIo;

public class MqttClient extends BaseIo {
    private MqttV5Connection connection;

    public MqttClient(Config config, EventBus bus) {
        super(config, bus);
        this.config.resisterConfigType("mqttClient", new ConfigType<>(MqttConfig.class));
    }

    @Override
    public void run() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'run'");
    }

}
