package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Humidity;
import ovh.angrysoft.homedaemon.devices.traits.Pressure;
import ovh.angrysoft.homedaemon.devices.traits.Temperature;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class WeatherV1 extends ZigbeeBaseDevice implements Temperature, Humidity, Pressure {

    public WeatherV1(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "WSDCGQ11LM"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("humidity", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("pressure", 0));
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

    @Override
    public int getPressure() {
        return status.get("pressure");
    }

}
