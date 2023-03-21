package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.traits.Contact;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb04 extends BaseDevice implements Contact {
    public Snzb04(DeviceInfo deviceInfo, Gateway gateway) {
        try {
            this.status.registerAttribute(new DeviceAttribute<>("contact", false));
            this.status.registerAttribute(new DeviceAttribute<>("battery_low", false));
            this.status.registerAttribute(new DeviceAttribute<>("voltage", false));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());

    }

    public boolean isContact() {
        return this.status.get("contact");
    }

}
