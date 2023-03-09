package ovh.angrysoft.homedaemon.discover;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class DeviceDiscovery {
    private Map<String, DeviceDiscoverInfo> deviceCache;

    public DeviceDiscovery() {
        this.deviceCache = new HashMap<>();
    }

    public DeviceDiscoverInfo discover(String sid, DiscoverEngine engine) {
        if (!this.deviceCache.containsKey(sid)) {
            ArrayList<DeviceDiscoverInfo> devicesInfo = engine.search();
            for (DeviceDiscoverInfo devInfo : devicesInfo) {
                this.deviceCache.put(sid, devInfo);
            }
        }

        return this.deviceCache.get(sid);
    }
}
