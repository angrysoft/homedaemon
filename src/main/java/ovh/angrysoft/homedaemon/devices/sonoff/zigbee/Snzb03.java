package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.traits.Motion;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb03 extends BaseDevice implements Motion {
    public Snzb03(DeviceInfo deviceInfo, Gateway gateway) {
        try {
            this.status.registerAttribute(new DeviceAttribute<>("occupancy", false));
            this.status.registerAttribute(new DeviceAttribute<>("battery_low", false));
            this.status.registerAttribute(new DeviceAttribute<>("voltage", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());
    }

    public boolean getOccupancy() {
        return status.get("occupancy");
    }

}
