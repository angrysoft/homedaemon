package ovh.angrysoft.homedaemon.devices.yeelight;

import java.util.logging.Level;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.Rgb;
import ovh.angrysoft.homedaemon.devices.traits.RgbColor;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class Color extends DeskLamp implements Rgb, RgbColor {
    public Color(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<Integer>("rgb", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("sat", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("hue", 0));
        } catch (AttributeAlreadyExist e) {
            logger.log(Level.ALL, "{0}", e.getMessage());
        }
    }

    public void setRgb(Integer red, Integer green, Integer blue) {
        this.api.setRGB(red, green, blue);
    }

    public void setColor(Integer rgb) {
        this.api.setColor(rgb);
    }

    @Override
    public void setup() {
        super.setup();
        try {
            this.status.update("minCt", 1700);
        } catch (AttributeReadOnly e) {
        }
        this.api.setMinCt(1700);
    }
}
