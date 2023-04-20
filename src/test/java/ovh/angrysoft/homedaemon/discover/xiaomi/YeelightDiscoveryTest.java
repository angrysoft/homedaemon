package ovh.angrysoft.homedaemon.discover.xiaomi;

import java.util.Set;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.discover.DeviceDiscoverInfo;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDiscovery;

public class YeelightDiscoveryTest {
    @Test
    @Tag("IntegrationTest")
    public void testDiscovery() {
        YeelightDiscovery discovery = new YeelightDiscovery();
        Set<DeviceDiscoverInfo> devInfo = discovery.search();
        for (DeviceDiscoverInfo dev : devInfo) {
            YeelightDeviceInfo yDev = (YeelightDeviceInfo) dev;
            System.out.print(yDev.getDeviceSid() + " ");
            System.out.print(yDev.get("addr") + " ");
            System.out.print(yDev.get("port") + " ");
            System.out.println(yDev.get("model").toString());
        }

    }

}
