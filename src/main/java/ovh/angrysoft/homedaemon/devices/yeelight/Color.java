package ovh.angrysoft.homedaemon.devices.yeelight;

import java.util.logging.Level;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.traits.Rgb;
import ovh.angrysoft.homedaemon.devices.traits.RgbColor;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

class Color  extends DeskLamp implements Rgb, RgbColor {
    public Color(YeelightDeviceInfo info) {
        super(info);
        this.api.setMinCt(1700);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("rgb", info.getRGB()));
            this.status.registerAttribute(new DeviceAttribute<>("sat", info.getSat()));
            this.status.registerAttribute(new DeviceAttribute<>("hue", info.getHue()));
        } catch (AttributeAlreadyExist e) {
            LOGGER.log(Level.ALL, "{0}", e.getMessage());
        }

    }

    public void setRgb(int red, int green, int blue) {
        this.api.setRGB(red, green, blue);
    }

    public void setColor(int rgb) {
        this.api.setColor(rgb);
    }
}