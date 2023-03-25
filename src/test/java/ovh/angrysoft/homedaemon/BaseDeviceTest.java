
package ovh.angrysoft.homedaemon;

import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.devices.traits.Toggle;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

import java.util.HashMap;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;

public class BaseDeviceTest {
    BaseDevice device;

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
}

class DummyDevice extends BaseDevice implements OnOff, Toggle {

    public DummyDevice(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            status.registerAttribute(new DeviceAttribute<>("power", "off"));
        } catch ( AttributeAlreadyExist e) {}
    }


    public void on() {}
    public void off() {}
    public boolean isOff() {
        return true;
    }

    public boolean isOn() {
        return false;
    }

    public void toggle() {}

}