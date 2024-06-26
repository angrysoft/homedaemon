package ovh.angrysoft.homedaemon.devices;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import ovh.angrysoft.homedaemon.DummyDevice;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class FakeDeviceManager implements DeviceManager {
    private HashMap<String, BaseDevice> devices;

    public FakeDeviceManager() {
        this.devices = new HashMap<>();
    }

    public void loadDeviceInfo() {
        HashMap<String, String> name = new HashMap<>();
        name.put("pl", "Lampa");
        HashMap<String, String> place = new HashMap<>();
        name.put("pl", "Salon");
        DeviceInfo deviceInfo = new DeviceInfo("123", "light", "diy", "superLight", name, place, "", new HashMap<>());
        BaseDevice device = new DummyDevice(deviceInfo);
        devices.put("123", device);
    }

    public void setupDevices() {
        throw new UnsupportedOperationException("Unimplemented method 'setup'");
    }

    public void execute(String sid, String cmd, Optional<Object> args) {
        throw new UnsupportedOperationException("Unimplemented method 'execute'");
    }

    public void update(Event statusEvent) {

        BaseDevice dev = this.devices.get(statusEvent.getSid());
        try {
            dev.status.update(statusEvent.getName(), statusEvent.getValue());
        } catch (AttributeReadOnly e) {
            e.printStackTrace();
        }
    }

    public <T> T queryStatus(String sid, String attrName) {
        BaseDevice dev = this.devices.get(sid);
        return dev.query(attrName);
    }

    @Override
    public EventBus getBus() {
        throw new UnsupportedOperationException("Unimplemented method 'getBus'");
    }

    @Override
    public BaseDevice getDevice(String sid) {
        throw new UnsupportedOperationException("Unimplemented method 'getDevice'");
    }

    @Override
    public List<Map<String,Object>> getDevicesList() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getDevicesList'");
    }

}
