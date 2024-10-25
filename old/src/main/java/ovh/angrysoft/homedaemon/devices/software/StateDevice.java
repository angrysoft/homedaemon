package ovh.angrysoft.homedaemon.devices.software;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class StateDevice extends BaseDevice {
    public StateDevice(DeviceInfo deviceInfo) {
        super(deviceInfo);
    }

    public <T> void registerStateAttribute(DeviceAttribute<T> deviceAttribute) {
        try {
            this.status.registerAttribute(deviceAttribute);
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void setup() {}
}
