package ovh.angrysoft.homedaemon;


import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.config.Config;
import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class App {
    public static void main(String[] args) {
        String devDir = System.getenv("DEVDIR");
        String confDir = System.getenv("CONFDIR");
        
        Config config = new Config();
        config.loadConfigs(confDir);
        Logger logger = Logger.getLogger("Homedaemon");
        if (config.get("homed", "debug").getAsBoolean()) {
            System.setProperty("java.util.logging.SimpleFormatter.format", "%1$tF %1$tT %2$s - %4$s: %5$s%6$s%n");
            logger.setLevel(Level.FINE);
        } else {
            System.setProperty("java.util.logging.SimpleFormatter.format", "[ %4$s ] %5$s%6$s%n");
            logger.setLevel(Level.WARNING);
        }


        EventBus bus = new EventBus();
        bus.addTrigger(new Trigger("status.*", (Event event) -> {
            System.out.println("handled event: " + Arrays.toString(event.getTopicList()));
        }));

        DeviceManager manger = new DeviceManager(devDir, bus);
        manger.loadDevice();
        logger.info("HomeDaemon Started");
        manger.setup();
    }
}
