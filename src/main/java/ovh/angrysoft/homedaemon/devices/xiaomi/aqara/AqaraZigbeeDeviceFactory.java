package ovh.angrysoft.homedaemon.devices.xiaomi.aqara;

import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.ZigbeeGateway;

public class AqaraZigbeeDeviceFactory {
    public static BaseDevice getDevice(DeviceInfo deviceInfo, ZigbeeGateway gateway) {
        switch (deviceInfo.getModel()) {
            case "QBKG04LM":
                return new CtrlNeutral(deviceInfo, gateway);
            case "QBKG03LM":
                return new CtrlNeutral2(deviceInfo, gateway);
            case "GZCGQ01LM":
                return new LightIntensitySensor(deviceInfo, gateway);
            case "MCCGQ01LM":
                return new Magnet(deviceInfo, gateway);
            case "ZNCZ02LM":
                return new Plug(deviceInfo, gateway);
            case "WSDCGQ01LM":
                return new SensorHt(deviceInfo, gateway);
            case "RTCGQ11LM":
                return new SensorMotionAq2(deviceInfo, gateway);
            case "WXKG11LM":
                return new SensorSwitchAq2(deviceInfo, gateway);
            case "WSDCGQ11LM":
                return new WeatherV1(deviceInfo, gateway);
            case "WXKG01LM":
                return new WirelessSwitch(deviceInfo, gateway);
        }
        return null;
    }
}
