package ovh.angrysoft.homedaemon;

import java.util.logging.Level;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.automation.AutomationManager;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Topic;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.config.ConfigBak;
import ovh.angrysoft.homedaemon.devices.HomedaemonDeviceManager;
import ovh.angrysoft.homedaemon.io.IOManager;

public class App {
    public static void main(String[] args) {
        String devDir = System.getenv("DEVICE.DIR");
        String confDir = System.getenv("CONFIG.DIR");
        String automationDir = System.getenv("AUTOMATION.DIR");
        if (devDir == null || confDir == null || automationDir == null) {
            System.err.println("Add env DEVICE.DIR CONFIG.DIR AUTOMATION.DIR");
            return;
        }
        Logger logger = Logger.getLogger("Homedaemon");
        ConfigBak config = new ConfigBak();
        config.loadConfigs(confDir);
        Level logLevel = Level.WARNING;
        String logFormat = "[ %4$s ] %5$s%6$s%n";
        if (config.get("homed", "debug").getAsBoolean()) {
            logFormat = "%1$tF %1$tT %2$s - %4$s: %5$s%6$s%n";
            logLevel = Level.FINE;
        }
        System.setProperty("java.util.logging.SimpleFormatter.format", logFormat);
        logger.setLevel(logLevel);
        // logger.getHandlers()[0].setLevel(logLevel);

        EventBus bus = new EventBus();
        bus.addTrigger(new Trigger(Topic.fromString("status.*"), (Event event) -> {
            logger.info(String.format("handled event: %s with payload: %s", event.getTopic().toString(),
                    event.getPayload()));
        }));

        bus.addTrigger(new Trigger(Topic.fromString("*"), (Event event) -> {
            logger.fine(String.format("debug msg: %s with payload: %s", event.getTopic().toString(),
                    event.getPayload()));
        }));

        HomedaemonDeviceManager deviceManager = new HomedaemonDeviceManager(devDir, bus);
        deviceManager.loadDeviceInfo();
        deviceManager.setupDevices();
        logger.info(String.format("HomeDaemon Started thread : %s", Thread.currentThread()));

        AutomationManager automationManager = new AutomationManager(automationDir, bus, deviceManager);
        automationManager.loadAutomation();

        // IOManager ioManager = new IOManager(config.get("homed", "io"), bus);
        // ioManager.loadIO();

        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                logger.severe(e.getMessage());
            }
        }
    }
}
