package ovh.angrysoft.homedaemon.devices.software;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class StateDevice extends BaseDevice {
    public StateDevice(DeviceInfo deviceInfo) {
        super(deviceInfo);
    }

    public <T> void registerStateAttribute(String stateName, T stateValue) {
        try {
            this.status.registerAttribute(new DeviceAttribute<T>(stateName, stateValue, false, false));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

    @Override
    public void setup() {
    }
}
