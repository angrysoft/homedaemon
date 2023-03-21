package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.traits.Dimmer;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

class Mono extends BaseDevice implements OnOff, Dimmer {
    protected YeelightApi api;

    public Mono(YeelightDeviceInfo info) {
        try {
            this.status.registerAttribute(new DeviceAttribute<>("power", info.getPower()));
            this.status.registerAttribute(new DeviceAttribute<>("color_mode", info.getColorMode()));
            this.status.registerAttribute(new DeviceAttribute<>("bright", info.getBright()));
            this.api = new YeelightApi(info.getAddr(), info.getPort());
        } catch (AttributeAlreadyExist e) {
            e.printStackTrace();
        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }

    public void on() {
        this.api.setPower(true);
    }

    public void off() {
        this.api.setPower(false);
    }

    public boolean isOn() {
        return (String) this.status.get("power") == "on";
    }

    public void setBright(int value) {
        this.api.setBright(value);
    }

    public int getBright() {
        return this.status.get("bright");
    }
}
