package ovh.angrysoft.homedaemon.devices.xiaomi;

import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.Gateway;
import ovh.angrysoft.homedaemon.devices.ZigbeeBaseDevice;
import ovh.angrysoft.homedaemon.devices.traits.OnOff;
import ovh.angrysoft.homedaemon.devices.traits.Toggle;

public class Plug extends ZigbeeBaseDevice implements OnOff, Toggle {

    public Plug(DeviceInfo deviceInfo, Gateway gateway) {
        super(deviceInfo, gateway);
        //TODO Auto-generated constructor stub
    }

    @Override
    public void toggle() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'toggle'");
    }

    @Override
    public void on() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'on'");
    }

    @Override
    public void off() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'off'");
    }

    @Override
    public boolean isOn() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'isOn'");
    }
    
}
