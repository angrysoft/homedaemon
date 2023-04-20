package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.traits.Contact;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb04 extends BaseDevice implements Contact {
    public Snzb04(DeviceInfo deviceInfo, Gateway gateway) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<Boolean>("contact", false));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("battery_low", false));
            this.status.registerAttribute(new DeviceAttribute<Integer>("voltage", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());

    }

    public boolean isContact() {
        return this.status.get("contact");
    }

}
