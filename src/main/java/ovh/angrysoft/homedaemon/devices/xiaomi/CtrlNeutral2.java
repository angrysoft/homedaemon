package ovh.angrysoft.homedaemon.devices.xiaomi;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.DoubleSwitch;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class CtrlNeutral2 extends ZigbeeBaseDevice implements DoubleSwitch {

    public CtrlNeutral2(DeviceInfo deviceInfo, Gateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("model", "QBKG03LM"));
            this.status.registerAttribute(new DeviceAttribute<>("state_left", ""));
            this.status.registerAttribute(new DeviceAttribute<>("state_right", ""));
            this.status.registerAttribute(new DeviceAttribute<>("device_temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<>("operation_mode_left", ""));
            this.status.registerAttribute(new DeviceAttribute<>("operation_mode_right", ""));
            this.status.registerAttribute(new DeviceAttribute<>("action", "", false, true));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());

    }

    public void left(boolean state) {
        this.setDevice("state_left", state ? "ON" : "OFF");
    }

    public void right(boolean state) {
        this.setDevice("state_right", state ? "ON" : "OFF");
    }

    public boolean isLeftOn() {
        return this.status.get("state_left").equals("ON");

    }

    public boolean isRightOn() {
        return this.status.get("state_right").equals("ON");
    }

    public void toggleLeft() {
        this.setDevice("state_right", "toggle");
    }

    public void toggleRight() {
        this.setDevice("state_right", "toggle");
    }

    public void setLeftDecoupled() {
        this.setDevice("operation_mode_left", "decoupled");
    }

    public void setRightDecoupled() {
        this.setDevice("operation_mode_right", "decoupled");
    }

    public void setLeftRelay() {
        this.setDevice("operation_mode_right", "control_left_relay");
    }

    public void setRightRelay() {
        this.setDevice("operation_mode_right", "control_right_relay");
    }
}
