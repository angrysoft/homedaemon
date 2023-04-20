package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class ZigbeeBaseDevice extends BaseDevice {
    protected Gateway gateway;

    public ZigbeeBaseDevice(DeviceInfo deviceInfo, Gateway gateway) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<Integer>("linkquality", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("voltage", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        this.gateway = gateway;
    }

}