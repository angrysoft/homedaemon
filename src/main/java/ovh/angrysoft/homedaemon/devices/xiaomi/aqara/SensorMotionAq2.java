package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Illuminance;
import ovh.angrysoft.homedaemon.devices.traits.Motion;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class SensorMotionAq2 extends ZigbeeBaseDevice implements Motion, Illuminance {

    public SensorMotionAq2(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("model", "RTCGQ11LM"));
            this.status.registerAttribute(new DeviceAttribute<>("occupancy", false));
            this.status.registerAttribute(new DeviceAttribute<>("illuminance", 0));
            this.status.registerAttribute(new DeviceAttribute<>("illuminance_lux", 0));
            this.status.registerAttribute(new DeviceAttribute<>("device_temperature", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());
    }

    public boolean getOccupancy() {
        return status.get("occupancy");
    }

    public int getIlluminance() {
        return this.status.get("illuminance");
    }

}
