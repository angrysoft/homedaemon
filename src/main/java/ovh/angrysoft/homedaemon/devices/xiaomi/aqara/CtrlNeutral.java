package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.AttributeUpdateBehavior;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class CtrlNeutral extends ZigbeeBaseDevice implements OnOff {

    public CtrlNeutral(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "QBKG04LM"));
            this.status.registerAttribute(new DeviceAttribute<String>("state", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("operation_mode", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("action", "", false, AttributeUpdateBehavior.ALWAYS));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }

    }

    public void on() {
        this.gateway.sendSet(this.status.get("sid"), "state", "ON");
    }

    public void off() {
        this.gateway.sendSet(this.status.get("sid"), "state", "OFF");
    }

    public boolean isOn() {
        return this.status.get("state").equals("ON");
    }

    public void setDecoupled() {
        this.gateway.sendSet(this.getSid(), "operation_mode", "decoupled");
    }

    public void setRelay() {
        this.gateway.sendSet(this.getSid(), "operation_mode", "control_relay");
    }

}
