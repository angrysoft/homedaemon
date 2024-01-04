package ovh.angrysoft.homedaemon.devices.sonoff;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.DoubleSwitch;
import ovh.angrysoft.homedaemon.discover.engines.EwelinkDiscoverEngine;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.watcher.EwelinkWatcher;

public class T52C86 extends BaseDevice implements DoubleSwitch {
    EwelinkApi api;

    public T52C86(DeviceInfo deviceInfo) {
        super(deviceInfo);
        this.discoverable = true;
        this.discoverEngine = new EwelinkDiscoverEngine();
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("ip", "localhost"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("port", 0));
            this.status.registerAttribute(new DeviceAttribute<String>("lightSwitch", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("lightMode", -1));
            this.status.registerAttribute(new DeviceAttribute<String>("startup", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("pulse", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("pulseWidth", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("rrsi", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("ssid", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("shock", -1));
            this.status.registerAttribute(new DeviceAttribute<String>("outlet0", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("outlet1", ""));
            this.status.registerAttribute(
                    new DeviceAttribute<String>("token", deviceInfo.getArgs().get("token")));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void setup() {
        this.api =
                new EwelinkApi(status.get("ip"), status.get("port"), getSid(), status.get("token"));
        this.watcher = EwelinkWatcher.getInstance();
        EwelinkWatcher.registerDevice(getSid(), status.get("token"));
    }

    @Override
    public void left(Boolean state) {
        api.setSwitches(state, 0);
    }

    @Override
    public void right(Boolean state) {
        api.setSwitches(state, 1);
    }

    @Override
    public boolean isLeftOn() {
        return status.get("outlet0").equals("on");
    }

    @Override
    public boolean isRightOn() {
        return status.get("outlet1").equals("on");
    }

    @Override
    public void toggleLeft() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'toggleLeft'");
    }

    @Override
    public void toggleRight() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'toggleRight'");
    }

    @Override
    public void allOn() {
        left(true);
        right(true);
    }

    @Override
    public void allOff() {
        left(false);
        right(false);
    }

}
