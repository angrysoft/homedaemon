package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.Brightness;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.discover.engines.YeelightDiscoveryEngine;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;
import ovh.angrysoft.homedaemon.watcher.YeelightWatcher;

public class Mono extends BaseDevice implements OnOff, Brightness {
    protected YeelightApi api;
    private static final String POWER = "power";

    public Mono(DeviceInfo deviceInfo) {
        super(deviceInfo);
        this.discoverable = true;
        //TODO: this need to be a Singelton 
        this.discoverEngine = new YeelightDiscoveryEngine();
        try {
            this.status.registerAttribute(new DeviceAttribute<String>(POWER, ""));
            this.status.addAlias("state", POWER);
            this.status.registerAttribute(new DeviceAttribute<Integer>("color_mode", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("bright", 0));
            this.status.registerAttribute(new DeviceAttribute<String>("addr", "localhost"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("port", 0));
        } catch (AttributeAlreadyExist | AttributeNotFound e) {
            logger.warning(e.getMessage());
        }
    }

    public void on() {
        this.api.setPower(true);
    }

    public void off() {
        this.api.setPower(false);
    }

    public boolean isOn() {
        return this.status.get(POWER).equals("on");
    }

    public void setBright(Integer value) {
        this.api.setBright(value);
    }

    public int getBright() {
        return this.status.get("bright");
    }

    @Override
    public void setup() {
        this.api = new YeelightApi(status.get("addr"), status.get("port"));
        this.watcher = new YeelightWatcher(getSid(), status.get("addr"), status.get("port"));
    }
}
