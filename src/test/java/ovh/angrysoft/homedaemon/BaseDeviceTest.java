
package ovh.angrysoft.homedaemon;

import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.devices.DeviceInfo;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.HashMap;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;

public class BaseDeviceTest {
    DummyDevice device;

    @BeforeEach
    void setUp() {
        HashMap<String, String> name = new HashMap<>();
        name.put("pl", "Lampa");
        HashMap<String, String> place = new HashMap<>();
        name.put("pl", "Salon");
        DeviceInfo deviceInfo = new DeviceInfo("aaaaaabbb", "light", "diy", "superLight", name, place, new HashMap<>());
        device = new DummyDevice(deviceInfo);
    }

    @Test
    @DisplayName("Get Device status")
    void testGetDeviceStatus() {
        System.out.println(device.getDeviceStatus());
    }

    @Test
    @DisplayName("Execute command")
    void testExecute() {
        assertEquals("off", this.device.query("power"));
        this.device.execute("on", null);
        assertEquals("on", this.device.query("power"));

    }

    @Test
    @DisplayName("Execute command witch args")
    void testExecuteWitchArgs() {
        assertEquals(0, (Integer) this.device.query("state"));
        this.device.execute("changeState", 5);
        assertEquals(5, (Integer) this.device.query("state"));

    }

    @Test
    @DisplayName("Execute command not allowed")
    void testExecuteNotAllowed() {
        assertEquals("off", this.device.query("power"));
        this.device.execute("off", null);
        assertEquals("off", this.device.query("power"));


    }
}