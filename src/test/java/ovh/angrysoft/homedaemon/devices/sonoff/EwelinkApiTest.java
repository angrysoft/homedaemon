package ovh.angrysoft.homedaemon.devices.sonoff;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class EwelinkApiTest {
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
}
