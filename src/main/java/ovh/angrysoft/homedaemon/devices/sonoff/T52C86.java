package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.switches.DoubleSwitch;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class T52C86 extends T586 implements DoubleSwitch {

    public T52C86(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("outlet0", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("outlet1", ""));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void outlet0(Boolean state) {
        api.setSwitches(state, 0);
    }

    @Override
    public void outlet1(Boolean state) {
        api.setSwitches(state, 1);
    }

    @Override
    public boolean isOutlet0On() {
        return status.get("outlet0").equals("on");
    }

    @Override
    public boolean isOutlet1On() {
        return status.get("outlet1").equals("on");
    }

    @Override
    public void toggleOutlet0() {
        outlet0(!isOutlet0On());
    }

    @Override
    public void toggleOutlet1() {
        outlet1(!isOutlet1On());
    }



    @Override
    public void allOn() {
        outlet0(true);
        outlet1(true);
        api.setLightSwitch(true);
    }

    @Override
    public void allOff() {
        outlet0(false);
        outlet1(false);
        api.setLightSwitch(false);
    }

}
