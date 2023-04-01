package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;
import ovh.angrysoft.homedaemon.devices.traits.Motion;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb03 extends BaseDevice implements Motion {
    public Snzb03(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<Boolean>("occupancy", false));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("battery_low", false));
            this.status.registerAttribute(new DeviceAttribute<Integer>("voltage", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());
    }

    public boolean getOccupancy() {
        return status.get("occupancy");
    }

}
