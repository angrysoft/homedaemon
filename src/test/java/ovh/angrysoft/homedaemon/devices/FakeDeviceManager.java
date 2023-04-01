package ovh.angrysoft.homedaemon.devices;

import java.util.HashMap;

import ovh.angrysoft.homedaemon.DummyDevice;
import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class FakeDeviceManager implements DeviceManager{
    private HashMap<String, BaseDevice> devices;

    public void loadDevice() {
        HashMap<String, String> name = new HashMap<>();
        name.put("pl", "Lampa");
        HashMap<String, String> place = new HashMap<>();
        name.put("pl", "Salon");
        DeviceInfo deviceInfo = new DeviceInfo("123", "light", "diy", "superLight", name, place, new HashMap<>());
        BaseDevice device = new DummyDevice(deviceInfo);
        devices.put("123", device);
    }

    public void setup() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'setup'");
    }

    public void execute(String sid, String cmd, Object args) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'execute'");
    }

    public void update(StatusEvent statusEvent) {
        System.out.println(statusEvent.getSid());

        BaseDevice dev = this.devices.get(statusEvent.getSid());
        try {
            dev.status.update(statusEvent);
        } catch (AttributeReadOnly e) {
            e.printStackTrace();
        }
    }

    public <T> T query(String sid, String attrName) {
        BaseDevice dev = this.devices.get(sid);
        DeviceAttribute<T> attr = dev.query(attrName);
        return attr.getValue();
    }
    
}
