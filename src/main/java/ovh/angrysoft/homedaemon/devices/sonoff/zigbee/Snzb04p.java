package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb04p extends Snzb04 {
    public Snzb04p(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "SNZB-04P"));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("tamper", false));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }

    }
}
