package ovh.angrysoft.homedaemon.devices.software;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Clock extends BaseDevice {

    protected Clock(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<Integer>("hour", -1));
            this.status.registerAttribute(new DeviceAttribute<Integer>("minute", -1));
            this.status.registerAttribute(new DeviceAttribute<Integer>("second", -1));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

}
