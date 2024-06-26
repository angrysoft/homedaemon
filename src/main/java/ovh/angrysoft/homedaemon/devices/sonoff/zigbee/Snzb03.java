package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.occupancy.OccupancySensing;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb03 extends ZigbeeBaseDevice implements OccupancySensing {
    public Snzb03(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "SNZB-03"));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("occupancy", false));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("battery_low", false));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    public boolean getOccupancy() {
        return status.get("occupancy");
    }

}
