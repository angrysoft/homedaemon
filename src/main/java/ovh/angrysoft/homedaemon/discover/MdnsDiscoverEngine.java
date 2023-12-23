package ovh.angrysoft.homedaemon.discover;

import java.io.IOException;
import java.net.InetAddress;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import javax.jmdns.JmDNS;
import javax.jmdns.ServiceEvent;
import javax.jmdns.ServiceInfo;
import javax.jmdns.ServiceListener;

public class MdnsDiscoverEngine extends DiscoverEngine {
    private String type;

    public MdnsDiscoverEngine(String type) {
        this.type = type;
    }

    @Override
    public Set<DeviceDiscoverInfo> search() {
        Set<DeviceDiscoverInfo> results = new HashSet<>();
        try (JmDNS jmdns = JmDNS.create(InetAddress.getLocalHost())) {
            jmdns.addServiceListener(type, new DiscoverListener());
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
        ServiceInfo info = event.getInfo();
        System.out.println("type: " + info.getType());
        System.out.println("addr: " + Arrays.toString(info.getHostAddresses()));
        System.out.println("port: " + info.getPort());

        Iterator<String> propertyNames = info.getPropertyNames().asIterator();
        while (propertyNames.hasNext()) {
            String name = propertyNames.next();
            System.out.print(name);
            System.out.println(" : " + info.getPropertyString(name));

        }



    }


}
