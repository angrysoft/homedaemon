package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Contact;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Magnet extends ZigbeeBaseDevice implements Contact {

    public Magnet(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "MCCGQ01LM"));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("contact", false));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

    @Override
    public boolean isContact() {
        return this.status.get("contact");
    }

}
