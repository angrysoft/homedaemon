package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import java.util.HashMap;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.zigbee2mqtt.Zigbee2MqttGateway;

public class CtrlNeutral2Test {
    @Test
    @DisplayName("test send cmd")
    @Tag("IntegrationTest")
    public void testOn() {
        DeviceInfo deviceInfo = new DeviceInfo("0x00158d0002bffe5a", "switch", "aqara", "QBKG03LM",
                null, null, "", null);

        HashMap<String, String> args = new HashMap<>();
        args.put("uri", "tcp://192.168.10.4:1883");
        args.put("user", "homedaemon");
        args.put("password", "spyb0tk34s");
        DeviceInfo gatewayInfo =
                new DeviceInfo("zigbee2mqtt", "gateway", "zigbee2mqtt", null, null, null, "", args);
        Zigbee2MqttGateway gateway = new Zigbee2MqttGateway(gatewayInfo);
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        CtrlNeutral2 ctrl = new CtrlNeutral2(deviceInfo);
        ctrl.setGateway(gateway);
        ctrl.setup();
        ctrl.outlet0(true);
        ctrl.outlet1(true);
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        // assertTrue(ctrl.isRightOn());
        // assertTrue(ctrl.isLeftOn());

        ctrl.outlet0(false);
        ctrl.outlet1(false);

    }
}
