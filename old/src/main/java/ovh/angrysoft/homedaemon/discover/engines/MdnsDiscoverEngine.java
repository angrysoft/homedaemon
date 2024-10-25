package ovh.angrysoft.homedaemon.discover.engines;

import java.io.IOException;
import java.net.InetAddress;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import javax.jmdns.JmDNS;
import javax.jmdns.ServiceEvent;
import javax.jmdns.ServiceInfo;
import javax.jmdns.ServiceListener;
import ovh.angrysoft.homedaemon.discover.DiscoverEngine;


public class MdnsDiscoverEngine extends DiscoverEngine {
    private String type;

    public MdnsDiscoverEngine(String type) {
        this.type = type;
    }

    @Override
    public Set<Map<String, Object>> search() {
        Set<Map<String, Object>> results = new HashSet<>();
        try (JmDNS jmdns = JmDNS.create(InetAddress.getLocalHost())) {
            jmdns.addServiceListener(type, new DiscoverListener(results));
            Thread.sleep(3000);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        return results;
    }

}


/**
 * DiscoverListener
 */
class DiscoverListener implements ServiceListener {
    Set<Map<String, Object>> deviceInfo;

    public DiscoverListener(Set<Map<String, Object>> deviceInfo) {
        this.deviceInfo = deviceInfo;
    }

    @Override
    public void serviceAdded(ServiceEvent event) {
        // there are no interesting information listen for serviceResoled.
    }

    @Override
    public void serviceRemoved(ServiceEvent event) {
        // there are no interesting information listen for serviceResoled.
    }

    @Override
    public void serviceResolved(ServiceEvent event) {
        Map<String, Object> devInfo = new HashMap<>();
        ServiceInfo info = event.getInfo();
        devInfo.put("ip", info.getHostAddresses()[0]);
        devInfo.put("port", info.getPort());
        Iterator<String> propertyNames = info.getPropertyNames().asIterator();
        while (propertyNames.hasNext()) {
            String name = propertyNames.next();
            devInfo.put(name, info.getPropertyString(name));
        }
        deviceInfo.add(devInfo);
    }
}
