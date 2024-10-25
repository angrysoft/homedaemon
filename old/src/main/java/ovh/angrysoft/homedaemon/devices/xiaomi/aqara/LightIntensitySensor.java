package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.Illuminance;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class LightIntensitySensor extends ZigbeeBaseDevice implements Illuminance<Integer> {

    public LightIntensitySensor(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "GZCGQ01LM"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("illuminance", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("illuminance_lux", 0));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    public void requestOfIlluminanceInfo() {
        this.gateway.sendGet(getSid(), "illuminance", "");
    }

    public void requestOfIlluminanceLuxInfo() {
        this.gateway.sendGet(getSid(), "illuminance_lux", "");
    }

    public Integer getIlluminance() {
        return this.status.get("illuminance");
    }

    @Override
    public void setup() {
        super.setup();
        this.requestOfIlluminanceInfo();
        this.requestOfIlluminanceLuxInfo();
    }

}
