package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.Dimmer;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;
import ovh.angrysoft.homedaemon.watcher.YeelightWatcher;

class Mono extends BaseDevice implements OnOff, Dimmer {
    protected YeelightApi api;

    public Mono(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("power", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("color_mode", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("bright", 0));
            this.status.registerAttribute(new DeviceAttribute<String>("addr", "localhost"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("port", 0));
        } catch (AttributeAlreadyExist e) {
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

    @Override
    public void setup() {
        try {
            this.api = new YeelightApi(status.get("addr"), status.get("port"));
        } catch (DeviceConnectionError e) {
            LOGGER.warning(e.getMessage());
        }
        this.watcher = new YeelightWatcher(getSid(), status.get("addr"), status.get("port"));
    }
}
