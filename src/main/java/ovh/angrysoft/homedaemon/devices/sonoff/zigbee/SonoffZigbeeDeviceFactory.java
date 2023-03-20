package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;

public class SonoffZigbeeDeviceFactory {

    public static BaseDevice getDevice(DeviceInfo deviceInfo, Gateway gateway) {
        switch (deviceInfo.getModel()) {
            case "SNZB-03":
                return new Snzb03(deviceInfo, gateway);
        }
        return null;
    }

}
