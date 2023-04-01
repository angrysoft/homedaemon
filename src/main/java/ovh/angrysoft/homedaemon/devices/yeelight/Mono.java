package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.Dimmer;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

class Mono extends BaseDevice implements OnOff, Dimmer {
    protected YeelightApi api;

    public Mono(DeviceInfo deviceInfo, YeelightDeviceInfo initData) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("power", initData.getPower()));
            this.status.registerAttribute(new DeviceAttribute<Integer>("color_mode", initData.getColorMode()));
            this.status.registerAttribute(new DeviceAttribute<Integer>("bright", initData.getBright()));
            this.api = new YeelightApi(initData.getAddr(), initData.getPort());
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
        return this.status.get("power").equals("on");
    }

    public void setBright(Integer value) {
        this.api.setBright(value);
    }

    public int getBright() {
        return this.status.get("bright");
    }
}
