package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.PressureReport;
import ovh.angrysoft.homedaemon.devices.traits.humidity.HumidityReport;
import ovh.angrysoft.homedaemon.devices.traits.temperature.TemperatureReport;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class WeatherV1 extends ZigbeeBaseDevice implements TemperatureReport, HumidityReport, PressureReport {

    public WeatherV1(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "WSDCGQ11LM"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("humidity", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("pressure", 0));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
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
