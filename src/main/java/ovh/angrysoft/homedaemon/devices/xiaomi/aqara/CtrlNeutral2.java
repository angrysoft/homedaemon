package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.AttributeUpdateBehavior;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.DoubleSwitch;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class CtrlNeutral2 extends ZigbeeBaseDevice implements DoubleSwitch {

    public CtrlNeutral2(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "QBKG03LM"));
            this.status.registerAttribute(new DeviceAttribute<String>("outlet0", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("outlet1", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("device_temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<String>("operation_mode_left", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("operation_mode_right", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("action", "", false,
                    AttributeUpdateBehavior.ALWAYS));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }

    }

    public void one(Boolean state) {
        this.gateway.sendSet(this.getSid(), "state_left", state ? "ON" : "OFF");
    }

    public void two(Boolean state) {
        this.gateway.sendSet(this.getSid(), "state_right", state ? "ON" : "OFF");
    }

    public boolean isOneOn() {
        return ((String) this.status.get("outlet0")).equalsIgnoreCase("on");
    }

    public boolean isTwoOn() {
        return ((String) this.status.get("outlet1")).equalsIgnoreCase("on");
    }

    public void toggleOne() {
        this.gateway.sendSet(this.getSid(), "state_left", "toggle");
    }

    public void toggleTwo() {
        this.gateway.sendSet(this.getSid(), "state_right", "toggle");
    }

    public void setLeftDecoupled() {
        this.gateway.sendSet(this.getSid(), "operation_mode_left", "decoupled");
    }

    public void setRightDecoupled() {
        this.gateway.sendSet(this.getSid(), "operation_mode_right", "decoupled");
    }

    public void setLeftRelay() {
        this.gateway.sendSet(this.getSid(), "operation_mode_right", "control_left_relay");
    }

    public void setRightRelay() {
        this.gateway.sendSet(this.getSid(), "operation_mode_right", "control_right_relay");
    }

    @Override
    public void allOn() {
        this.gateway.sendSet(this.getSid(), "state_left", "ON");
        this.gateway.sendSet(this.getSid(), "state_right", "ON");
    }

    @Override
    public void allOff() {
        this.gateway.sendSet(this.getSid(), "state_left", "OFF");
        this.gateway.sendSet(this.getSid(), "state_right", "OFF");
    }
}
