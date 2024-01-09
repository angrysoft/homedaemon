package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.DoubleSwitch;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;

public class T52C86 extends T586 implements DoubleSwitch {

    public T52C86(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("outlet0", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("outlet1", ""));
            this.status.addAlias("state_left", "outlet0");
            this.status.addAlias("state_right", "outlet1");
        } catch (AttributeAlreadyExist | AttributeNotFound e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void one(Boolean state) {
        api.setSwitches(state, 0);
    }

    @Override
    public void two(Boolean state) {
        api.setSwitches(state, 1);
    }

    @Override
    public boolean isOneOn() {
        return status.get("outlet0").equals("on");
    }

    @Override
    public boolean isTwoOn() {
        return status.get("outlet1").equals("on");
    }

    @Override
    public void toggleOne() {
        one(!isOneOn());
    }

    @Override
    public void toggleTwo() {
        two(!isTwoOn());
    }



    @Override
    public void allOn() {
        one(true);
        two(true);
        api.setLightSwitch(true);
    }

    @Override
    public void allOff() {
        one(false);
        two(false);
        api.setLightSwitch(false);
    }

}
