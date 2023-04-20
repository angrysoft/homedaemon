package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.traits.Humidity;
import ovh.angrysoft.homedaemon.devices.traits.Temperature;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Snzb02 extends BaseDevice implements Temperature, Humidity {
    public Snzb02(DeviceInfo deviceInfo, Gateway gateway) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<Integer>("temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("humidity", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("voltage", 0));
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
