package ovh.angrysoft.homedaemon.devices.xiaomi;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class CtrlNeutral extends ZigbeeBaseDevice implements OnOff {

    public CtrlNeutral(DeviceInfo deviceInfo, Gateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("model", "QBKG04LM"));
            this.status.registerAttribute(new DeviceAttribute<>("state", ""));
            this.status.registerAttribute(new DeviceAttribute<>("operation_mode", ""));
            this.status.registerAttribute(new DeviceAttribute<>("action", "", false, true));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());

    }

    public void on() {
        this.gateway.send(this.status.get("sid"), "{\"state\": \"ON\"}");
    }
    
    public void off() {
        this.gateway.send(this.status.get("sid"), "{\"state\": \"OFF\"}");
    }

    public boolean isOn() {
        return this.status.get("state").equals("ON");
    }

    public void setDecoupled() {
        this.setDevice("operation_mode", "decoupled");
    }

    public void setRelay() {
        this.setDevice("operation_mode", "control_relay");
    }

    
}
