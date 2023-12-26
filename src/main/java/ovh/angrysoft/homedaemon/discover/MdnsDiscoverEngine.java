package ovh.angrysoft.homedaemon.discover;

import java.io.IOException;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import javax.jmdns.JmDNS;
import javax.jmdns.ServiceEvent;
import javax.jmdns.ServiceInfo;
import javax.jmdns.ServiceListener;
import ovh.angrysoft.homedaemon.discover.ewelink.EwelinkDeviceInfo;
import static java.util.Map.Entry;
import static java.util.Map.entry;


public class MdnsDiscoverEngine extends DiscoverEngine {
    private String type;

    public MdnsDiscoverEngine(String type) {
        this.type = type;
    }

    @Override
    public Set<DeviceDiscoverInfo> search() {
        Set<DeviceDiscoverInfo> results = new HashSet<>();
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
    Set<DeviceDiscoverInfo> deviceInfo;

    public DiscoverListener(Set<DeviceDiscoverInfo> deviceInfo) {
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
        EwelinkDeviceInfo devInfo = new EwelinkDeviceInfo();
        ServiceInfo info = event.getInfo();
        devInfo.set("ip", info.getHostAddresses()[0]);
        devInfo.set("port", info.getPort());
        Iterator<String> propertyNames = info.getPropertyNames().asIterator();
        while (propertyNames.hasNext()) {
            String name = propertyNames.next();
            devInfo.set(name, info.getPropertyString(name));
        }

        String data = (String) devInfo.get("data1");

        if (Boolean.parseBoolean((String) devInfo.get("encrypt"))) {
            System.err.println("is enctyrpted");

        }
        System.err.println(data);

    }

    List<Entry<String, Object>> parseData(String data) {
        List<Entry<String, Object>> entrys = new ArrayList<>();
        entrys.add(entry("dupa", "blada"));
        return entrys;
    }
}
