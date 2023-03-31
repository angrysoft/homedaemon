package ovh.angrysoft.homedaemon.devices.yeelight;

import java.util.logging.Level;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.Rgb;
import ovh.angrysoft.homedaemon.devices.traits.RgbColor;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

class Color  extends DeskLamp implements Rgb, RgbColor {
    public Color(DeviceInfo deviceInfo, YeelightDeviceInfo initData) {
        super(deviceInfo, initData);
        this.api.setMinCt(1700);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("rgb", initData.getRGB()));
            this.status.registerAttribute(new DeviceAttribute<>("sat", initData.getSat()));
            this.status.registerAttribute(new DeviceAttribute<>("hue", initData.getHue()));
        } catch (AttributeAlreadyExist e) {
            LOGGER.log(Level.ALL, "{0}", e.getMessage());
        }

    }

    public void setRgb(Integer red, Integer green, Integer blue) {
        this.api.setRGB(red, green, blue);
    }

    public void setColor(Integer rgb) {
        this.api.setColor(rgb);
    }
}
