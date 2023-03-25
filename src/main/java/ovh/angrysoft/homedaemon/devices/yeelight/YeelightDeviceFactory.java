package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;

public class YeelightDeviceFactory {
    public static BaseDevice getDevice(DeviceInfo deviceInfo, YeelightDeviceInfo yeelightDeviceInfo) {
        switch (yeelightDeviceInfo.getModel()) {
            case "mono":
                return new Mono(deviceInfo, yeelightDeviceInfo);
            case "desklamp":
                return new DeskLamp(deviceInfo, yeelightDeviceInfo);
            case "color":
            case "bslamp1":
                return new Color(deviceInfo, yeelightDeviceInfo);
        }
        return null;
    }
}
