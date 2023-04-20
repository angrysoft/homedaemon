package ovh.angrysoft.homedaemon.devices.yeelight;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.ColorTemperature;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public class DeskLamp extends Mono implements ColorTemperature {

    public DeskLamp(DeviceInfo deviceInfo, YeelightDeviceInfo initData) {
        super(deviceInfo, initData);
        try {
            this.status.registerAttribute(new DeviceAttribute<Integer>("ct", initData.get("ct")));

        } catch (AttributeAlreadyExist e) {
            e.printStackTrace();
        }
        this.api.setMinCt(2700);
        this.api.setMaxCt(6500);
    }

    public void setCtPc(Integer pc) {
        this.api.setCtPc(pc);
    }

    public int getCtPc() {
        int pc = ((int) status.get("ct") - this.api.getMinCt()) / (this.api.getMaxCt() - this.api.getMinCt());
        return pc;
    }
}
