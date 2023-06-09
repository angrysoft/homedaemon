package ovh.angrysoft.homedaemon.automation;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.automation.conditions.AndCondition;
import ovh.angrysoft.homedaemon.automation.conditions.Condition;
import ovh.angrysoft.homedaemon.automation.conditions.NotCondition;
import ovh.angrysoft.homedaemon.automation.conditions.OrCondition;
import ovh.angrysoft.homedaemon.automation.conditions.StatusTestCase;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.devices.DeviceManager;
import ovh.angrysoft.homedaemon.devices.FakeDeviceManager;

public class ConditionTest {
    private DeviceManager deviceManager;

    @BeforeEach
    public void setUp() {
        deviceManager = new FakeDeviceManager();
        deviceManager.loadDeviceInfo();
    }

    @Test
    public void testAndCondition() {
        // Given
        Condition condition = new AndCondition(deviceManager);
        condition.addCase(new StatusTestCase("status", "123", "stringState", "enabled"));
        condition.addCase(new StatusTestCase("status", "123", "state", 4));
        deviceManager.update(Event.statusEvent("123", "stringState", "enabled"));
        deviceManager.update(Event.statusEvent("123", "state", 4));
        // When
        Boolean conditionResult = condition.check();
        // Then
        assertTrue(conditionResult);
    }

    @Test
    public void testAndConditionFalse() {
        // Given
        Condition condition = new AndCondition(deviceManager);
        condition.addCase(new StatusTestCase("status", "123", "stringState", "disabled"));
        condition.addCase(new StatusTestCase("status", "123", "state", 4));
        deviceManager.update(Event.statusEvent("123", "stringState", "enabled"));
        deviceManager.update(Event.statusEvent("123", "state", 4));
        // When
        Boolean conditionResult = condition.check();
        // Then
        assertFalse(conditionResult);
    }

    @Test
    public void testOrCondition() {
        // Given
        Condition condition = new OrCondition(deviceManager);
        condition.addCase(new StatusTestCase("status", "123", "stringState", "enabled"));
        condition.addCase(new StatusTestCase("status", "123", "state", 4));
        deviceManager.update(Event.statusEvent("123", "stringState", "enabled1"));
        deviceManager.update(Event.statusEvent("123", "state", 4));
        // When
        Boolean conditionResult = condition.check();
        // Then
        assertTrue(conditionResult);
    }

    @Test
    public void testOrConditionFalse() {
        // Given
        Condition condition = new OrCondition(deviceManager);
        condition.addCase(new StatusTestCase("status", "123", "stringState", "enabled"));
        condition.addCase(new StatusTestCase("status", "123", "state", 4));
        deviceManager.update(Event.statusEvent("123", "stringState", "enabled1"));
        deviceManager.update(Event.statusEvent("123", "state", 5));
        // When
        Boolean conditionResult = condition.check();
        // Then
        assertFalse(conditionResult);
    }

    @Test
    public void testNotCondition() {
        // Given
        Condition condition = new NotCondition(deviceManager);
        condition.addCase(new StatusTestCase("status", "123", "stringState", "enabled"));
        condition.addCase(new StatusTestCase("status", "123", "state", 4));
        deviceManager.update(Event.statusEvent("123", "stringState", "enabled1"));
        deviceManager.update(Event.statusEvent("123", "state", 5));
        // When
        Boolean conditionResult = condition.check();
        // Then
        assertTrue(conditionResult);
    }

    @Test
    public void testNotConditionFalse() {
        // Given
        Condition condition = new NotCondition(deviceManager);
        condition.addCase(new StatusTestCase("status", "123", "stringState", "enabled"));
        condition.addCase(new StatusTestCase("status", "123", "state", 4));
        deviceManager.update(Event.statusEvent("123", "stringState", "enabled"));
        deviceManager.update(Event.statusEvent("123", "state", 5));
        // When
        Boolean conditionResult = condition.check();
        // Then
        assertFalse(conditionResult);
    }
}
