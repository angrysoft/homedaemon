package ovh.angrysoft.homedaemon.discover.ewelink;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import ovh.angrysoft.homedaemon.discover.DeviceDiscoverInfo;

public class EwelinkDeviceInfo implements DeviceDiscoverInfo{
    private Map<String, Object> info = new HashMap<>();
    
    @Override
    public String getDeviceSid() {
        return (String) info.get("sid");
    }

    public synchronized void set(String key, Object value) {
        this.info.put(key, value);
    }

    public synchronized void setEntry(Entry<String, Object> ent) {
        info.put(ent.getKey(), ent.getValue());
    }

    @Override
    public Object get(String key) {
        return info.get(key);
    }

    @Override
    public boolean containsKey(String key) {
        return info.containsKey(key);
    }

    @Override
    public Set<Entry<String, Object>> entrySet() {
        return info.entrySet();
    }
    
}
