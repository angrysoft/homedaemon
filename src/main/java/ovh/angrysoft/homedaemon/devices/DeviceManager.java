package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;

public interface DeviceManager {
    public void loadDeviceInfo();

    public void setupDevices();

    public void execute(String sid, String cmd, Object args);

    public void update(StatusEvent statusEvent);

    public <T> T queryStatus(String sid, String attr);

    public EventBus getBus();

    public BaseDevice getDevice(String sid);
}
