package ovh.angrysoft.homedaemon.devices.tuya;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.devices.traits.Toggle;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class TS0011 extends ZigbeeBaseDevice implements OnOff, Toggle {

    public TS0011(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "TS0011"));
            this.status.registerAttribute(new DeviceAttribute<String>("state", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("power_on_behavior", ""));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

    public void on() {
        this.gateway.sendSet(getSid(), "state", "ON");
    }

    public void off() {
        this.gateway.sendSet(getSid(), "state", "OFF");
    }

    public void toggle() {
        this.gateway.sendSet(getSid(), "state", "toggle");
    }

    public boolean isOn() {
        return this.status.get("state").equals("ON");
    }

    public void setPowerOnBehavior(PowerOnBehaviorStatus status) {
        this.gateway.sendSet(getSid(), "power_on_behavior", status.toString());
    }

    public String getPowerOnBehavior() {
        return this.status.get("power_on_behavior");
    }

}
