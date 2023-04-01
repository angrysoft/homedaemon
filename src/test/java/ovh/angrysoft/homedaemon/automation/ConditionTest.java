package ovh.angrysoft.homedaemon.automation;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.devices.DeviceManager;
import ovh.angrysoft.homedaemon.devices.FakeDeviceManager;

public class ConditionTest {
    private DeviceManager deviceManager;

    @BeforeEach
    public void setUp() {
        deviceManager = new FakeDeviceManager();
    }

    @Test
    public void testAndCases() {
        deviceManager.update(new StatusEvent("123", "stringState", "enabled"));
        String o = deviceManager.query("123", "stringState");
        System.out.println(o);
    }
}
