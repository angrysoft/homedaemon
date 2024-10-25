package ovh.angrysoft.homedaemon.automation.conditions;

import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class OrCondition extends Condition {

    public OrCondition(DeviceManager deviceManager) {
        super(deviceManager);
    }

    @Override
    public boolean check() {
        for (TestCase<?> testCase : this.cases) {
            var value = deviceManager.queryStatus(testCase.getDeviceSid(), testCase.getAttrName());
            if (testCase.check(value))
                return true;
        }
        return false;
    }
    
}
