package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Humidity;
import ovh.angrysoft.homedaemon.devices.traits.Temperature;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class SensorHt extends ZigbeeBaseDevice implements Temperature, Humidity {

    public SensorHt(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "WSDCGQ01LM"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("humidity", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

    public int getHumidity() {
        return status.get("humidity");
    }

    public int getTemp() {
        return status.get("temperature");
    }

}
