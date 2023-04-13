package ovh.angrysoft.homedaemon.devices.software;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class ClockDevice extends BaseDevice {

    public ClockDevice(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("time", ""));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

}
