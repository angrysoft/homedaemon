package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.AttributeUpdateBehavior;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class SensorSwitchAq2 extends ZigbeeBaseDevice {

    public SensorSwitchAq2(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "WXKG11LM"));
            this.status.registerAttribute(new DeviceAttribute<String>("action", "", false,
                    AttributeUpdateBehavior.ALWAYS));
            this.status.registerAttribute(new DeviceAttribute<Integer>("device_temperature", 0));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }
}
