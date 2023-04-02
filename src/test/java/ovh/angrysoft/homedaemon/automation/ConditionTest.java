package ovh.angrysoft.homedaemon.automation;

import static org.junit.jupiter.api.Assertions.assertTrue;

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
        deviceManager.loadDevice();
    }

    @Test
    public void testAndCases() {
        //Given
        Case condition = new Case("and");
        condition.addCase(new Case("status", "123", "stringState", "enable"));
        condition.addCase(new Case("status", "123", "state", 4));
        deviceManager.update(new StatusEvent("123", "stringState", "enabled"));
        deviceManager.update(new StatusEvent("123", "state", 4));
        //When
        Boolean conditionResult = condition.check();
        //Then
        var o = deviceManager.queryStatus("123", "stringState");
        System.out.println(o.toString());
        assertTrue(conditionResult);
    }
}
