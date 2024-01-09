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
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }
    @Override
    public void allOff() {
        super.allOff();
        three(false);
    }
    
    @Override
    public void three(Boolean state) {
        api.setSwitches(state, 2);
    }
    
    @Override
    public boolean isThreeOn() {
        return status.get("outlet2").equals("on");
    }
    
    @Override
    public void toggleThree() {
        three(!isThreeOn());
    }
}
