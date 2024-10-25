package ovh.angrysoft.homedaemon.automation.conditions;

import java.util.HashSet;
import java.util.Set;

import ovh.angrysoft.homedaemon.devices.DeviceManager;

public abstract class Condition {
    Set<TestCase<?>> cases;
    DeviceManager deviceManager;

    Condition(DeviceManager deviceManager) {
        this.deviceManager = deviceManager;
        this.cases = new HashSet<>();
    }

    public abstract boolean check();

    public void addCase(TestCase<?> testCase) {
        this.cases.add(testCase);
    }
}
