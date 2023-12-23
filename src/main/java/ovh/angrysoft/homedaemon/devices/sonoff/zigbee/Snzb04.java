package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Contact;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb04 extends ZigbeeBaseDevice implements Contact {
    public Snzb04(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "SNZB-04"));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("contact", false));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("battery_low", false));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }

    }

    public boolean isContact() {
        return this.status.get("contact");
    }

}
