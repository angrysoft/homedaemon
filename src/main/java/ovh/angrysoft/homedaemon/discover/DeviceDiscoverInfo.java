package ovh.angrysoft.homedaemon.discover;

import java.util.Map.Entry;
import java.util.Set;

public interface DeviceDiscoverInfo {
    public String getDeviceSid();

    public Object get(String key);

    public boolean containsKey(String key);

    public Set<Entry<String, Object>> entrySet();  
}
