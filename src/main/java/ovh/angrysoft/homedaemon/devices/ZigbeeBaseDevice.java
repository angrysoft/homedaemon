package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class ZigbeeBaseDevice extends BaseDevice {
    protected Gateway gateway;

    public ZigbeeBaseDevice(DeviceInfo deviceInfo, Gateway gateway) {
        try {
            this.status.registerAttribute(new DeviceAttribute<>("linkquality", 0));
            this.status.registerAttribute(new DeviceAttribute<>("voltage", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        this.gateway = gateway;
    }

    protected void setDevice(String cmd, String value) {
        this.gateway.send(this.status.get("sid"), String.format("{\"%s\": \"%s\"}", cmd, value));
    }
}