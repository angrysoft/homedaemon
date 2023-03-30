package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import java.util.HashMap;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.zigbee2mqtt.Zigbee2MqttGateway;

public class PlugTest {
    @Test
    @DisplayName("test send cmd")
    @Tag("IntegrationTest")
    public void toggle() {
        DeviceInfo deviceInfo = new DeviceInfo("0x00158d00027d0065", "switch", "aqara",
            "QBKG03LM", null, null, null);

        HashMap<String, String> args = new HashMap<>();
        args.put("uri", "tcp://192.168.10.4:1883");
        args.put("user", "homedaemon");
        args.put("password", "spyb0tk34s");
        DeviceInfo gatewayInfo = new DeviceInfo("zigbee2mqtt", "gateway", "zigbee2mqtt", null, null, null, args);
        Zigbee2MqttGateway gateway = new Zigbee2MqttGateway(gatewayInfo);
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        Plug plug = new Plug(deviceInfo, gateway);
        plug.on();
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        plug.off();

    }
}
