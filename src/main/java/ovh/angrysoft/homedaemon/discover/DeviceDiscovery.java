package ovh.angrysoft.homedaemon.discover;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import ovh.angrysoft.homedaemon.exceptions.discover.DeviceNotDiscovered;

public class DeviceDiscovery {
    private Map<String, Map<String, Object>> deviceCache;

    public DeviceDiscovery() {
        this.deviceCache = new HashMap<>();
    }

    public Map<String, Object> discover(String sid, DiscoverEngine engine)
            throws DeviceNotDiscovered {
        if (!this.deviceCache.containsKey(sid)) {

            Set<Map<String, Object>> devicesInfo = engine.search();

            for (Map<String, Object> devInfo : devicesInfo) {
                this.deviceCache.put((String) devInfo.get("sid"), devInfo);
            }
        }
        Map<String, Object> result = this.deviceCache.get(sid);
        if (result == null)
            throw new DeviceNotDiscovered("Can't discover device: " + sid);

        return result;
    }
}
