package ovh.angrysoft.homedaemon.devices.sonoff.zigbee;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;

public class SonoffZigbeeDeviceFactory {

    public static BaseDevice getDevice(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        switch (deviceInfo.getModel()) {
            case "SNZB-01":
                return new Snzb01(deviceInfo, gateway);
            case "SNZB-02":
                return new Snzb02(deviceInfo, gateway);
            case "SNZB-03":
                return new Snzb03(deviceInfo, gateway);
            case "SNZB-04":
                return new Snzb04(deviceInfo, gateway);
        }
        return null;
    }

}
