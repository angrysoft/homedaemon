
package ovh.angrysoft.homedaemon;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.HashMap;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.devices.DeviceInfo;

public class BaseDeviceTest {
    DummyDevice device;

    @BeforeEach
    void setUp() {
        HashMap<String, String> name = new HashMap<>();
        name.put("pl", "Lampa");
        HashMap<String, String> place = new HashMap<>();
        name.put("pl", "Salon");
        DeviceInfo deviceInfo = new DeviceInfo("aaaaaabbb", "light", "diy", "superLight", name, place, "", new HashMap<>());
        device = new DummyDevice(deviceInfo);
    }

    @Test
    @DisplayName("Get Device status")
    void testGetDeviceStatus() {
        System.out.println(device.getDeviceStatus());
    }

    @Test
    @DisplayName("Get Device status")
    void testCommand() {
        System.out.println(this.device.getCommands());
        assertEquals(5, this.device.getCommands().size());
    }

    @Test
    @DisplayName("Execute command")
    void testExecute() {
        assertEquals("off", this.device.query("power"));
        this.device.execute("on", Optional.empty());
        assertEquals("on", this.device.query("power"));

    }

    @Test
    @DisplayName("Execute command witch args")
    void testExecuteWitchArgs() {
        assertEquals(0, (Integer) this.device.query("state"));
        this.device.execute("changeState", Optional.of(5));
        assertEquals(5, (Integer) this.device.query("state"));

    }

    @Test
    @DisplayName("Execute command not allowed")
    void testExecuteNotAllowed() {
        assertEquals("off", this.device.query("power"));
        this.device.execute("off", Optional.empty());
        assertEquals("off", this.device.query("power"));


    }
}