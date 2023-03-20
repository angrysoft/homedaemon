package ovh.angrysoft.homedaemon.discover;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import ovh.angrysoft.homedaemon.exceptions.discover.DeviceNotDiscovered;

public class DeviceDiscovery {
    private Map<String, DeviceDiscoverInfo> deviceCache;

    public DeviceDiscovery() {
        this.deviceCache = new HashMap<>();
    }

    public DeviceDiscoverInfo discover(String sid, DiscoverEngine engine) throws DeviceNotDiscovered {
        if (!this.deviceCache.containsKey(sid)) {
            Set<DeviceDiscoverInfo> devicesInfo = engine.search();
            
            for (DeviceDiscoverInfo devInfo : devicesInfo) {
                System.out.println("discover " + devInfo.getSid());
                this.deviceCache.put(devInfo.getSid(), devInfo);
            }
        }
        DeviceDiscoverInfo result = this.deviceCache.get(sid);
        if (result == null)
            throw new DeviceNotDiscovered("Can't discover device: " + sid);
        
        return result;
    }
}
