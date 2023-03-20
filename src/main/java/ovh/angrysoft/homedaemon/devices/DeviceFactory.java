package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.devices.sonoff.zigbee.SonoffZigbeeDeviceFactory;
import ovh.angrysoft.homedaemon.devices.yeelight.YeelightDeviceFactory;
import ovh.angrysoft.homedaemon.devices.zigbee2mqtt.Zigbee2MqttGateway;
import ovh.angrysoft.homedaemon.discover.DeviceDiscovery;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDiscovery;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceNotSupported;
import ovh.angrysoft.homedaemon.exceptions.discover.DeviceNotDiscovered;
import ovh.angrysoft.homedaemon.watcher.WatcherManager;
import ovh.angrysoft.homedaemon.watcher.YeelightWatcher;
import ovh.angrysoft.homedaemon.watcher.Zigbee2MqttWatcher;

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
            case "zigbee2mqtt":
                Zigbee2MqttGateway z2m = new Zigbee2MqttGateway(deviceInfo);
                watcherManager.registerWatcher(new Zigbee2MqttWatcher(z2m));
                return z2m;

        }

        throw new DeviceNotSupported(
                String.format("Device %s - %s not supported", deviceInfo.manufacturer, deviceInfo.model));
    }

    public BaseDevice getDevice(DeviceInfo deviceInfo, Gateway gateway) throws DeviceNotSupported, DeviceNotDiscovered {
        switch (deviceInfo.manufacturer) {
            case "sonoff":
                return SonoffZigbeeDeviceFactory.getDevice(deviceInfo, gateway);

        }

        throw new DeviceNotSupported(
                String.format("Device %s - %s not supported", deviceInfo.manufacturer, deviceInfo.model));
    }
}