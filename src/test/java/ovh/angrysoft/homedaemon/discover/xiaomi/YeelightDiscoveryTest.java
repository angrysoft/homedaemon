package ovh.angrysoft.homedaemon.discover.xiaomi;

import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import ovh.angrysoft.homedaemon.discover.engines.YeelightDiscoveryEngine;

class YeelightDiscoveryTest {
    @Test
    @Tag("IntegrationTest")
    void testDiscovery() {
        YeelightDiscoveryEngine discovery = new YeelightDiscoveryEngine();
        Set<Map<String, Object>> devInfo = discovery.search();
        for (Map<String, Object> dev : devInfo) {
            System.out.print(dev.get("sid") + " ");
            System.out.print(dev.get("addr") + " ");
            System.out.print(dev.get("port") + " ");
            System.out.println(dev.get("model").toString());
        }
    }

}
