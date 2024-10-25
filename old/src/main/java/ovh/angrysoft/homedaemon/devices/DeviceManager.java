package ovh.angrysoft.homedaemon.devices;

import java.util.List;
import java.util.Map;
import java.util.Optional;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;

public interface DeviceManager {
    public void loadDeviceInfo();

    public void setupDevices();

    public void execute(String sid, String cmd, Optional<Object> args);

    public void update(Event statusEvent);

    public <T> T queryStatus(String sid, String attr);

    public EventBus getBus();

    public BaseDevice getDevice(String sid);

    public List<Map<String,Object>> getDevicesList();
}
