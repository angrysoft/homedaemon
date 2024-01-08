package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;

public class T51C86 extends T586 implements OnOff {
    public T51C86(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("outlet0", ""));
            this.status.addAlias("state", "outlet0");
            this.status.registerAttribute(
                    new DeviceAttribute<String>("token", deviceInfo.getArgs().get("token")));
        } catch (AttributeAlreadyExist | AttributeNotFound e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void on() {
        api.setSwitches(true, 0);
    }

    @Override
    public void off() {
        api.setSwitches(false, 0);
    }

    @Override
    public boolean isOn() {
        return status.get("outlet0").equals("on");
    }

}
