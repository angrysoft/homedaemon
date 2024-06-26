package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.ColorTemperature;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class DeskLamp extends Mono implements ColorTemperature {

    public DeskLamp(DeviceInfo deviceInfo) {
        super(deviceInfo);
        try {
            this.status.registerAttribute(new DeviceAttribute<Integer>("ct", 0));
            this.status.registerAttribute(new DeviceAttribute<Integer>("minCt", 2700));
            this.status.registerAttribute(new DeviceAttribute<Integer>("maxCt", 6500));

        } catch (AttributeAlreadyExist e) {
            e.printStackTrace();
        }
    }

    public void setCtPc(Integer pc) {
        this.api.setCtPc(pc);
    }

    public int getCtPc() {
        return ((int) status.get("ct") - this.api.getMinCt()) / (this.api.getMaxCt() - this.api.getMinCt()) * 100;
    }

    @Override
    public void setup() {
        super.setup();
        this.api.setMinCt(2700);
        this.api.setMaxCt(6500);
    }
}
