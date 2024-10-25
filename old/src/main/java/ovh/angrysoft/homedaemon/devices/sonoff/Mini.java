package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.switches.SingleSwitch;
import ovh.angrysoft.homedaemon.discover.engines.EwelinkDiscoverEngine;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.watcher.EwelinkWatcher;

public class Mini extends BaseDevice implements SingleSwitch {
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
            this.status.registerAttribute(new DeviceAttribute<String>("outlet", ""));
        } catch (AttributeAlreadyExist e) {
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
    public void outlet(Boolean state) {
        api.setSwitch(state);
    }

    @Override
    public boolean isOutletOn() {
        return this.status.get("switch").equals("on");
    }

    @Override
    public void toggleOutlet() {
        outlet(!isOutletOn());
    }

}
