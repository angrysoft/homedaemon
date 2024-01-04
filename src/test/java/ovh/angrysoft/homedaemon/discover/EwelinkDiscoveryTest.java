package ovh.angrysoft.homedaemon.discover;


import java.util.Map;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import ovh.angrysoft.homedaemon.discover.engines.EwelinkDiscoverEngine;


class EwelinkDiscoveryTest {
    @Test
    @Tag("IntegrationTest")
    void testDiscovery() {
       
        var engine = new EwelinkDiscoverEngine();
        for (Map<String, Object> dev : engine.search()) {
            System.out.println(dev);
        }

    }

}

