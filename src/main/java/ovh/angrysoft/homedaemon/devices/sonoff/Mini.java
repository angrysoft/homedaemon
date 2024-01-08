package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.discover.engines.EwelinkDiscoverEngine;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;
import ovh.angrysoft.homedaemon.watcher.EwelinkWatcher;

public class Mini extends BaseDevice implements OnOff {
    EwelinkApi api;
    public Mini(DeviceInfo deviceInfo) {
        super(deviceInfo);
        this.discoverable = true;
        this.discoverEngine = new EwelinkDiscoverEngine();
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("ip", "localhost"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("port", 0));
            this.status.registerAttribute(new DeviceAttribute<String>("startup", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("pulse", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("pulseWidth", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("rrsi", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("ssid", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("sledOnline", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("power", ""));
            this.status.addAlias("state", "power");
        } catch (AttributeAlreadyExist | AttributeNotFound e) {
            logger.warning(e.getMessage());
        }
    }
    
    @Override
    public void setup() {
        this.api = new EwelinkApi(status.get("ip"), status.get("port"), getSid());
        this.watcher = EwelinkWatcher.getInstance();
        EwelinkWatcher.registerDevice(getSid());
    }

    @Override
    public void on() {
        api.setSwitch(true);
    }

    @Override
    public void off() {
        api.setSwitch(false);
    }

    @Override
    public boolean isOn() {
        return this.status.get("power").equals("on");
    }

}
