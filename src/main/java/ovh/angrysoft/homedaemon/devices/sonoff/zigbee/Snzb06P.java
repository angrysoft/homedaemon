package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.AttributeUpdateBehavior;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Illuminance;
import ovh.angrysoft.homedaemon.devices.traits.occupancy.OccupancySensing;
import ovh.angrysoft.homedaemon.devices.traits.occupancy.OccupancySettingsSensitivity;
import ovh.angrysoft.homedaemon.devices.traits.occupancy.OccupancySettingsTimeout;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb06P extends ZigbeeBaseDevice
        implements OccupancySensing, OccupancySettingsTimeout, OccupancySettingsSensitivity<String>, Illuminance {
    public Snzb06P(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "SNZB-06P"));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("occupancy", false));
            this.status.registerAttribute(new DeviceAttribute<Integer>("illuminance", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("occupancy_timeout", 10));
            // TODO enum
            this.status.registerAttribute(new DeviceAttribute<String>("occupancy_sensitivity", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("no_occupancy_since", 0,
                    false, AttributeUpdateBehavior.ALWAYS));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    public boolean getOccupancy() {
        return status.get("occupancy");
    }

    @Override
    public int getIlluminance() {
        return this.status.get("illuminance");
    }

    @Override
    public int getOccupancyTimeout() {
        return this.status.get("occupancy_timeout");
    }

    @Override
    public void setOccupancyTimeout(int value) {
        this.gateway.sendSet(getSid(), "occupancy_timeout", value);
    }

    @Override
    public String getOccupancySensitivity() {
        return this.status.get("occupancy_sensitivity");
    }

    @Override
    public void setOccupancySensitivity(String value) {
        this.gateway.sendSet(getSid(), "occupancy_sensitivity", value);
    }

}
