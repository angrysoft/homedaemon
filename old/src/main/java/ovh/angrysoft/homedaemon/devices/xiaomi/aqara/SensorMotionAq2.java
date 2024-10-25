package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.AttributeUpdateBehavior;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Illuminance;
import ovh.angrysoft.homedaemon.devices.traits.occupancy.OccupancySensing;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class SensorMotionAq2 extends ZigbeeBaseDevice implements OccupancySensing, Illuminance<Integer> {

    public SensorMotionAq2(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "RTCGQ11LM"));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("occupancy", false));
            this.status.registerAttribute(new DeviceAttribute<Integer>("illuminance", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("illuminance_lux", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("device_temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("no_occupancy_since", 0,
                    false, AttributeUpdateBehavior.ALWAYS));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    public boolean getOccupancy() {
        return status.get("occupancy");
    }

    public Integer getIlluminance() {
        return this.status.get("illuminance");
    }

}
