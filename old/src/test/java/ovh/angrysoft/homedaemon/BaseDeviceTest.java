
package ovh.angrysoft.homedaemon;

import static java.util.Map.entry;
import static org.junit.jupiter.api.Assertions.assertEquals;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;

class BaseDeviceTest {
    DummyDevice device;

    @BeforeEach
    void setUp() {
        HashMap<String, String> name = new HashMap<>();
        name.put("pl", "Lampa");
        HashMap<String, String> place = new HashMap<>();
        name.put("pl", "Salon");
        DeviceInfo deviceInfo = new DeviceInfo("aaaaaabbb", "light", "diy", "superLight", name,
                place, "", new HashMap<>());
        device = new DummyDevice(deviceInfo);
    }

    @Test
    @DisplayName("Get Device status")
    void testGetDeviceStatus() {
        List<String> traits = new ArrayList<>();
        traits.add("OnOff");
        traits.add("Toggle");
        Map<String, Object> expected =
                Map.ofEntries(entry("stringState", ""), entry("name", Map.of("pl", "Salon")),
                        entry("traits", traits), entry("place", new HashMap<>()),
                        entry("power", "off"), entry("state", 0), entry("sid", "aaaaaabbb"));

        assertEquals(expected, device.getDeviceStatus());
    }

    @Test
    @DisplayName("Device get Commands")
    void testGetCommand() {
        Set<String> expected = new HashSet<>();
        expected.add("isOn");
        expected.add("changeState");
        expected.add("toggle");
        expected.add("off");
        expected.add("on");
        assertEquals(expected, this.device.getCommands());
    }

    @Test
    @DisplayName("Device get Traits")
    void testGetAllTraits() {
        List<String> expected = new ArrayList<>();
        expected.add("OnOff");
        expected.add("Toggle");
        System.out.println(device.getTraits());
        assertEquals(expected, this.device.getTraits());
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
