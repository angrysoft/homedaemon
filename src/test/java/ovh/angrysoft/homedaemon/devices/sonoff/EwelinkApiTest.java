package ovh.angrysoft.homedaemon.devices.sonoff;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class EwelinkApiTest {
    String deviceKey = "fba25b03-dced-4a73-abc6-983a2488c8fd";
    @Test
    @Tag("IntegrationTest")
    void testSetSwitchOn() {
        EwelinkApi api = new EwelinkApi("192.168.10.18", 8081, "1000b6063e");
        api.setSwitch(true);
    }
    @Test
    @Tag("IntegrationTest")
    void testSetSwitchOff() {
        EwelinkApi api = new EwelinkApi("192.168.10.18", 8081, "1000b6063e");
        api.setSwitch(false);
    }

    @Test
    @Tag("IntegrationTest")
    void testSetSwitchesOn() {
        EwelinkApi api = new EwelinkApi("192.168.10.11", 8081, "1001f10ae4", deviceKey);
        api.setSwitches(true, 0);
    }
    @Test
    @Tag("IntegrationTest")
    void testSetlisthtSwitchOn() {
        EwelinkApi api = new EwelinkApi("192.168.10.11", 8081, "1001f10ae4", deviceKey);
        api.setLightSwitch(true);
    }

    @Test
    @Tag("IntegrationTest")
    void testSetlisthtSwitchOff() {
        EwelinkApi api = new EwelinkApi("192.168.10.11", 8081, "1001f10ae4", deviceKey);
        api.setLightSwitch(false);
    }

    @Test
    @Tag("IntegrationTest")
    void testSetSwitchesOff() {
        EwelinkApi api = new EwelinkApi("192.168.10.11", 8081, "1001f10ae4", deviceKey);
        api.setSwitches(false, 0);
    }
}
