package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;

public class YeelightDeviceFactory {
    public static BaseDevice getDevice(YeelightDeviceInfo yeelightDeviceInfo) {
        System.out.println("getModel: " + yeelightDeviceInfo.getModel());
        switch (yeelightDeviceInfo.getModel()) {
            case "mono":
                return new Mono(yeelightDeviceInfo);
            case "desklamp":
                return new DeskLamp(yeelightDeviceInfo);
            case "color":
            case "bslamp1":
                return new Color(yeelightDeviceInfo);
        }
        return null;
    }
}
