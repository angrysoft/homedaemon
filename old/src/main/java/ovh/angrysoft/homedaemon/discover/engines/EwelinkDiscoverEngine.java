package ovh.angrysoft.homedaemon.discover.engines;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;
import ovh.angrysoft.homedaemon.discover.DiscoverEngine;

public class EwelinkDiscoverEngine extends DiscoverEngine {

    @Override
    public Set<Map<String, Object>> search() {
        Set<Map<String, Object>> results = new HashSet<>();
        MdnsDiscoverEngine mdns = new MdnsDiscoverEngine("_ewelink._tcp.local.");
        for (Map<String, Object> item : mdns.search()) {
            Map<String, Object> deviceInfo = parseDevice(item);
            synchronized (this) {
                results.add(deviceInfo);
            }
        }
        return results;
    }

    private Map<String, Object> parseDevice(Map<String, Object> dev) {
        Map<String, Object> info = new HashMap<>();
        for (Entry<String, Object> entry : dev.entrySet()) {
            if (entry.getKey().equals("id")) {
                info.put("sid", entry.getValue());
            } else {
                info.put(entry.getKey(), entry.getValue());
            }
        }
        return info;
    }
}
