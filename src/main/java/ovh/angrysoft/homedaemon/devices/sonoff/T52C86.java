package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.DoubleOutlet;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;

public class T52C86 extends T586 implements DoubleOutlet {

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
    public void left(Boolean state) {
        api.setSwitches(state, 0);
    }

    @Override
    public void right(Boolean state) {
        api.setSwitches(state, 1);
    }

    @Override
    public boolean isLeftOn() {
        return status.get("outlet0").equals("on");
    }

    @Override
    public boolean isRightOn() {
        return status.get("outlet1").equals("on");
    }

    @Override
    public void toggleLeft() {
        left(!isLeftOn());
    }

    @Override
    public void toggleRight() {
        right(!isRightOn());
    }



    @Override
    public void allOn() {
        left(true);
        right(true);
        api.setLightSwitch(true);
    }
    
    @Override
    public void allOff() {
        left(false);
        right(false);
        api.setLightSwitch(false);
    }

}
