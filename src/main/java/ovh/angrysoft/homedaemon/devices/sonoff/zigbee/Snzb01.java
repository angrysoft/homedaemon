package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.AttributeUpdateBehavior;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb01 extends ZigbeeBaseDevice {
    public Snzb01(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("action", "", false,
                    AttributeUpdateBehavior.ALWAYS));
            this.status.registerAttribute(new DeviceAttribute<String>("model", "SNZB-01"));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

}
