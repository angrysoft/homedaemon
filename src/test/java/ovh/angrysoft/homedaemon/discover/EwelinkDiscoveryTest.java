package ovh.angrysoft.homedaemon.discover;


import java.util.Set;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;


class EwelinkDiscoveryTest {
    @Test
    @Tag("IntegrationTest")
    void testDiscovery() {
        MdnsDiscoverEngine mdns = new MdnsDiscoverEngine("_ewelink._tcp.local.");
        Set<DeviceDiscoverInfo> devInfo = mdns.search();
        for (DeviceDiscoverInfo dev : devInfo) {
            System.out.println(dev);
        }

    }

}

