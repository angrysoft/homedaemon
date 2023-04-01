package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;

public interface DeviceManager {
    public void loadDevice();
    public void setup();
    public void execute(String sid, String cmd, Object args);
    public void update(StatusEvent statusEvent);
    public <T> T query(String sid, String attr);
}
