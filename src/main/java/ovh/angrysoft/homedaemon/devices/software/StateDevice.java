package ovh.angrysoft.homedaemon.devices.software;

import java.util.Map;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class StateDevice extends BaseDevice {
    public StateDevice(DeviceInfo deviceInfo) {
        super(deviceInfo);
    }

    public void registerStateAttribute(String attrName, Map<String,Object> attrValue) {
        try {
            this.status.registerAttribute(new DeviceAttribute<Map<String,Object>>(attrName, attrValue, false, false));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

    
}
