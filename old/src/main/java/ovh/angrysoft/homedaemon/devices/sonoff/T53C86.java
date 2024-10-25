package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.switches.TripleSwitch;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

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
        outlet2(false);
    }

    @Override
    public void outlet2(Boolean state) {
        api.setSwitches(state, 2);
    }

    @Override
    public boolean isOutlet2On() {
        return status.get("outlet2").equals("on");
    }

    @Override
    public void toggleOutlet2() {
        outlet2(!isOutlet2On());
    }
}
