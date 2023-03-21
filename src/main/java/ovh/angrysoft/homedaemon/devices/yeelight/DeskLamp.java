package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.traits.ColorTemperature;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class DeskLamp extends Mono implements ColorTemperature {

    public DeskLamp(YeelightDeviceInfo info) {
        super(info);
        try {
            this.status.registerAttribute(new DeviceAttribute<>("ct", info.getCt()));

        } catch (AttributeAlreadyExist e) {
            e.printStackTrace();
        }
        this.api.setMinCt(2700);
        this.api.setMaxCt(6500);
    }

    public void setCtPc(int pc) {
        this.api.setCtPc(pc);
    }

    public int getCtPc() {
        int pc = ((int) status.get("ct") - this.api.getMinCt()) / (this.api.getMaxCt() - this.api.getMinCt());
        return pc;
    }
}
