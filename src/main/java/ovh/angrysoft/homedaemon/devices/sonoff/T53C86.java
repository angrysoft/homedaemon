package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.TripleSwitch;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;

public class T53C86 extends T52C86 implements TripleSwitch {

    public T53C86(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("outlet2", ""));
            this.status.addAlias("state_center", "outlet1");
            this.status.addAlias("state_right", "outlet2");
        } catch (AttributeAlreadyExist | AttributeNotFound e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void right(Boolean state) {
        api.setSwitches(state, 2);
    }

    @Override
    public boolean isRightOn() {
        return status.get("outlet2").equals("on");
    }

    @Override
    public void center(Boolean state) {
        api.setSwitches(state, 1);
    }

    @Override
    public boolean isCenterOn() {
        return status.get("outlet1").equals("on");
    }

    @Override
    public void toggleCenter() {
        center(! isCenterOn());
    }

    @Override
    public void allOff() {
        super.allOff();
        center(false);
    }
}
