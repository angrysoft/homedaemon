package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.devices.traits.Toggle;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class Plug extends ZigbeeBaseDevice implements OnOff, Toggle {

    public Plug(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        super(deviceInfo, gateway);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("model", "ZNCZ02LM"));
            this.status.registerAttribute(new DeviceAttribute<String>("state", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("power", 0));
            this.status.registerAttribute(new DeviceAttribute<Double>("energy", 0.0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("device_temperature", 0));
            this.status.registerAttribute(new DeviceAttribute<Boolean>("power_outage_memory", false));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

    public void requestOfPowerInfo() {
        this.gateway.sendGet(getSid(), "power", "");
    }

    public void requestOfPowerOutageMemoryInfo() {
        this.gateway.sendGet(getSid(), "power_outage_memory", "");
    }

    public void setPowerOutageMemory(boolean state) {
        this.gateway.sendSet(getSid(), "power_outage_memory", state);
    }

    public void toggle() {
        this.gateway.sendSet(getSid(), "state", "toggle");
    }

    public void on() {
        this.gateway.sendSet(getSid(), "state", "ON");
    }

    public void off() {
        this.gateway.sendSet(getSid(), "state", "OFF");
    }

    public boolean isOn() {
        return this.status.get("state").equals("ON");
    }

}
