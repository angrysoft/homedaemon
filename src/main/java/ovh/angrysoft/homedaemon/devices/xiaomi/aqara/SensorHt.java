package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Humidity;
import ovh.angrysoft.homedaemon.devices.traits.Temperature;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class SensorHt extends ZigbeeBaseDevice implements Temperature, Humidity {

    public SensorHt(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("model", "WSDCGQ01LM"));
            this.status.registerAttribute(new DeviceAttribute<>("temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<>("humidity", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());
    }

    public int getHumidity() {
        return status.get("humidity");
    }

    public int getTemp() {
        return status.get("temperature");
    }

}
