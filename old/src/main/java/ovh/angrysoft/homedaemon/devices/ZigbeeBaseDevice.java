package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class ZigbeeBaseDevice extends BaseDevice {
    protected Gateway gateway;

    public ZigbeeBaseDevice(DeviceInfo deviceInfo) {
        super(deviceInfo);
        this.gatewayNeeded = true;
        try {
            this.status.registerAttribute(new DeviceAttribute<Integer>("linkquality", 0, false,
                    AttributeUpdateBehavior.IGNORE));
            this.status.registerAttribute(new DeviceAttribute<Integer>("voltage", 0));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void setGateway(Gateway gateway) {
        this.gateway = gateway;
    }

    @Override
    public void setup() {
        gateway.registerSubDevice(status.get("sid"), status.get("model"));

    }

}
