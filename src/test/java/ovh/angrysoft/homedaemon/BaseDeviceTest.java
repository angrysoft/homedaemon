package ovh.angrysoft.homedaemon;

import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.traits.OnOff;
import ovh.angrysoft.homedaemon.traits.Toggle;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;

public class BaseDeviceTest {
    BaseDevice device;

    @BeforeEach
    void setUp() {
        device = new DummyDevice();
    }

    @Test
    @DisplayName("Get Device status")
    void testGetDeviceStatus() {
        System.out.println(device.getDeviceStatus());
    }
}

class DummyDevice extends BaseDevice implements OnOff, Toggle {

    public DummyDevice() {
        super();
        try {
            status.registerAttribute(new DeviceAttribute<>("power", false, "off"));
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

    public void Toggle() {}

}