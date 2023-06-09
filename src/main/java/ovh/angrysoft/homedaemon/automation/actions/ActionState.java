package ovh.angrysoft.homedaemon.automation.actions;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class ActionState extends Action {
    private DeviceManager deviceManager;
    private String attrName;
    private Object attrValue;

    public ActionState(String attrName, Object attrValue, DeviceManager deviceManager) {
        this.attrName = attrName;
        this.attrValue = attrValue;
        this.deviceManager = deviceManager;
    }

    @Override
    public void run() {
        deviceManager.update(Event.statusEvent("state", attrName, attrValue));
    }
}
