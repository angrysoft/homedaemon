/*
Copyright 2023 Sebastian Zwierzchowski aka Angrysoft

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package ovh.angrysoft.homedaemon;

import java.util.logging.Level;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.automation.AutomationManager;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Topic;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.config.Config;
import ovh.angrysoft.homedaemon.config.ConfigType;
import ovh.angrysoft.homedaemon.config.HomedConfig;
import ovh.angrysoft.homedaemon.devices.HomedaemonDeviceManager;
import ovh.angrysoft.homedaemon.io.IOManager;

public class App {
    public static void main(String[] args) {
        String devDir = System.getenv("DEVICE_DIR");
        String confDir = System.getenv("CONFIG_DIR");
        String automationDir = System.getenv("AUTOMATION_DIR");
        if (devDir == null || confDir == null || automationDir == null) {
            System.err.println("Add env DEVICE_DIR CONFIG_DIR AUTOMATION_DIR");
            return;
        }
        Logger logger = Logger.getLogger("Homedaemon");
        Config config = new Config(confDir);
        config.resisterConfigType("homed", new ConfigType<HomedConfig>(HomedConfig.class));
        Level logLevel = Level.WARNING;
        String logFormat = "[ %4$s ] %5$s%6$s%n";
        HomedConfig homedConfig = (HomedConfig) config.get("homed");
        if (homedConfig.debug()) {
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

        IOManager ioManager = new IOManager(homedConfig.io(), bus);
        ioManager.loadIO();

        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                logger.severe(e.getMessage());
            }
        }
    }
}
