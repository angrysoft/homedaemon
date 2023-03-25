package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class WirelessSwitch extends ZigbeeBaseDevice {

    public WirelessSwitch(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("model", "WXKG01LM"));
            this.status.registerAttribute(new DeviceAttribute<>("action", "", false, true));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());
    }

}
