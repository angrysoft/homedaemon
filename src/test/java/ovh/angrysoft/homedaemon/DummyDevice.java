package ovh.angrysoft.homedaemon;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.devices.traits.Toggle;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class DummyDevice extends BaseDevice implements OnOff, Toggle {

    public DummyDevice(DeviceInfo deviceInfo) {
        super(deviceInfo);
        this.commands.add("on");
        this.commands.add("changeState");

        try {
            status.registerAttribute(new DeviceAttribute<>("power", "off"));
            status.registerAttribute(new DeviceAttribute<>("state", 0));
        } catch ( AttributeAlreadyExist e) {}
    }


    public void on() {
        try {
            this.status.update(new StatusEvent("aaaaaabbb", "power", "on"));
        } catch (AttributeReadOnly e) {
            e.printStackTrace();
        }
    }
    public void off() {
        try {
            this.status.update(new StatusEvent("aaaaaabbb", "power", "off"));
        } catch (AttributeReadOnly e) {
            e.printStackTrace();
        }
    }
    
    public void changeState(Integer state) {
        try {
            this.status.update(new StatusEvent("aaaaaabbb", "state", state));
        } catch (AttributeReadOnly e) {
            e.printStackTrace();
        }
    }

    
    public boolean isOff() {
        return true;
    }

    public boolean isOn() {
        return false;
    }

    public void toggle() {}

}