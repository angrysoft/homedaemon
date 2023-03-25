package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class ZigbeeBaseDevice extends BaseDevice {
    protected ZigbeeGateway gateway;

    public ZigbeeBaseDevice(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("linkquality", 0));
            this.status.registerAttribute(new DeviceAttribute<>("voltage", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        this.gateway = gateway;
    }

}