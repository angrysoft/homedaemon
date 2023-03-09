package ovh.angrysoft.homedaemon.discover.xiaomi;

import java.util.ArrayList;

import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.discover.DeviceDiscoverInfo;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDeviceInfo;
import ovh.angrysoft.homedaemon.discover.yeelight.YeelightDiscovery;

public class YeelightDiscoveryTest {
    @Test
    public void testDiscovery() {
        YeelightDiscovery discovery = new YeelightDiscovery();
        ArrayList<DeviceDiscoverInfo> devInfo =  discovery.search();
        for (DeviceDiscoverInfo dev : devInfo) {
            YeelightDeviceInfo yDev = (YeelightDeviceInfo) dev;
            System.out.print(yDev.getSid() + " ");
            System.out.print(yDev.getAddr() + " ");
            System.out.print(yDev.getPort() + " ");
            System.out.println(yDev.getModel());
        }

    }

}
