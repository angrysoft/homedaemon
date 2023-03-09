package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.traits.Rgb;
import ovh.angrysoft.homedaemon.devices.traits.RgbColor;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;

public class Color  extends DeskLamp implements Rgb, RgbColor {
    public Color(YeelightDeviceInfo info) {
        super(info);
        this.api.setMinCt(1700);

    }

    public void setRgb(int red, int green, int blue) {
        this.api.setRGB(red, green, blue);
    }

    public void setColor(int rgb) {
        this.api.setColor(rgb);
    }
}
