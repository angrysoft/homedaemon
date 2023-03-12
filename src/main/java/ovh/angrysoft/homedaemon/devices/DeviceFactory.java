package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.devices.yeelight.YeelightDeviceFactory;
import ovh.angrysoft.homedaemon.discover.DeviceDiscovery;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDiscovery;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceNotSupported;
import ovh.angrysoft.homedaemon.exceptions.discover.DeviceNotDiscovered;
import ovh.angrysoft.homedaemon.watcher.WatcherManager;
import ovh.angrysoft.homedaemon.watcher.YeelightWatcher;

class DeviceFactory {
    private DeviceDiscovery deviceDiscovery;
    private WatcherManager watcherManager;

    public DeviceFactory(WatcherManager watcherManager) {
        this.deviceDiscovery = new DeviceDiscovery();
        this.watcherManager = watcherManager;
    }

    public BaseDevice getDevice(DeviceInfo deviceInfo) throws DeviceNotSupported, DeviceNotDiscovered {
        switch (deviceInfo.manufacturer) {
            case "yeelight":
                YeelightDeviceInfo yeelightDeviceInfo = (YeelightDeviceInfo) this.deviceDiscovery
                        .discover(deviceInfo.sid, new YeelightDiscovery());

                watcherManager.registerWatcher(new YeelightWatcher(yeelightDeviceInfo.getSid(),
                        yeelightDeviceInfo.getAddr(), yeelightDeviceInfo.getPort()));

                return YeelightDeviceFactory.getDevice(yeelightDeviceInfo);
        }

        throw new DeviceNotSupported(
                String.format("Device %s - %s not supported", deviceInfo.manufacturer, deviceInfo.model));
    }
}
