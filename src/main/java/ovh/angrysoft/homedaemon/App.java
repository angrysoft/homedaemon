package ovh.angrysoft.homedaemon;


import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.automation.AutomationManager;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.config.Config;
import ovh.angrysoft.homedaemon.devices.HomedaemonDeviceManager;

public class App {
    public static void main(String[] args) {
        String devDir = System.getenv("DEVICE.DIR");
        String confDir = System.getenv("CONFIG.DIR");
        String automationDir = System.getenv("AUTOMATION.DIR");
        
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
            logger.info(String.format("handled event: %s with payload: %s", Arrays.toString(event.getTopicList()), event.getPayload()));
        }));

        HomedaemonDeviceManager deviceManager = new HomedaemonDeviceManager(devDir, bus);
        deviceManager.loadDevice();
        deviceManager.setup();
        logger.info(String.format("HomeDaemon Started thread : %s", Thread.currentThread()));
        
        AutomationManager automationManager = new AutomationManager(automationDir, bus, deviceManager);
        automationManager.loadAutomation();
        
        while(true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                logger.severe(e.getMessage());
            }
        }
    }
}
