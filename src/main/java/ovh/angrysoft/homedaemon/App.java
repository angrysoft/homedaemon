package ovh.angrysoft.homedaemon;


import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class App {
    public static void main(String[] args) {
        String devDir = System.getenv("DEVDIR");
        String confDir = System.getenv("CONFDIR");
        System.out.println(devDir + " " + confDir);
        Logger logger = Logger.getLogger("Homedaemon");
        logger.setLevel(Level.FINE);
        EventBus bus = new EventBus();
        bus.addTrigger(new Trigger("status.*", (Event event) -> {
            System.out.println("handled event: " + Arrays.toString(event.getTopicList()));
        }));
        DeviceManager manger = new DeviceManager(devDir, bus);
        manger.loadDevice();
        manger.setup();
    }
}
