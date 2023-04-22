package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

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
            this.status.registerAttribute(new DeviceAttribute<String>("state_left", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("state_right", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("device_temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<String>("operation_mode_left", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("operation_mode_right", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("action", "", false, true));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }

    }

    public void left(Boolean state) {
        this.gateway.sendSet(this.getSid(), "state_left", state ? "ON" : "OFF");
    }

    public void right(Boolean state) {
        this.gateway.sendSet(this.getSid(), "state_right", state ? "ON" : "OFF");
    }

    public boolean isLeftOn() {
        return this.status.get("state_left").equals("ON");

    }

    public boolean isRightOn() {
        return this.status.get("state_right").equals("ON");
    }

    public void toggleLeft() {
        this.gateway.sendSet(this.getSid(), "state_left", "toggle");
    }

    public void toggleRight() {
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
