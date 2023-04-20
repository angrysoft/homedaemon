package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Illuminance;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class LightIntensitySensor extends ZigbeeBaseDevice implements Illuminance {

    public LightIntensitySensor(DeviceInfo deviceInfo, Gateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "GZCGQ01LM"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("illuminance", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("illuminance_lux", 0));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
        gateway.registerSubDevice(deviceInfo.getSid(), deviceInfo.getModel());
        this.requestOfIlluminanceInfo();
        this.requestOfIlluminanceLuxInfo();

    }

    public void requestOfIlluminanceInfo() {
        this.gateway.sendGet(getSid(), "illuminance", "");
    }

    public void requestOfIlluminanceLuxInfo() {
        this.gateway.sendGet(getSid(), "illuminance_lux", "");
    }

    public int getIlluminance() {
        return this.status.get("illuminance");
    }

}
