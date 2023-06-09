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

import java.util.Optional;
import java.util.logging.ConsoleHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import ovh.angrysoft.homedaemon.automation.AutomationManager;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Topic;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.config.Config;
import ovh.angrysoft.homedaemon.config.ConfigType;
import ovh.angrysoft.homedaemon.config.HomedConfig;
import ovh.angrysoft.homedaemon.devices.DeviceManager;
import ovh.angrysoft.homedaemon.devices.HomedaemonDeviceManager;
import ovh.angrysoft.homedaemon.io.IOManager;

public class App {
    static Logger logger = Logger.getLogger("Homedaemon");
    static Config config;

    public static void main(String[] args) {
        String devDir = System.getenv("DEVICE_DIR");
        String confDir = System.getenv("CONFIG_DIR");
        String automationDir = System.getenv("AUTOMATION_DIR");
        if (devDir == null || confDir == null || automationDir == null) {
            System.err.println("Add env DEVICE_DIR CONFIG_DIR AUTOMATION_DIR");
            return;
        }
        HomedConfig homedConfig = setupConfig(confDir);

        setupLogger(homedConfig.debug());

        EventBus bus = new EventBus();

        HomedaemonDeviceManager deviceManager = new HomedaemonDeviceManager(devDir, bus);
        deviceManager.loadDeviceInfo();
        deviceManager.setupDevices();
        setupDefaultsEvents(bus, deviceManager);

        AutomationManager automationManager = new AutomationManager(automationDir, bus, deviceManager);
        automationManager.loadAutomation();

        IOManager ioManager = new IOManager(config, bus);
        ioManager.loadIO();

        bus.dispatch(Event.statusEvent("homed", "init", "done"));

        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                logger.severe(e.getMessage());
            }
        }
    }

    private static void setupDefaultsEvents(EventBus bus, DeviceManager deviceManager) {
        bus.addTrigger(new Trigger(Topic.fromString("status.*"), (Event event) -> {
            logger.info(String.format("handled event: %s with payload: %s", event.getTopic().toString(),
                    event.getPayload()));
        }));

        bus.addTrigger(new Trigger(Topic.fromString("execute.*"), (Event event) -> {
            deviceManager.execute(event.getSid(), event.getName(), Optional.ofNullable(event.getValue()));
        }));
    }

    private static void setupLogger(boolean isDebug) {
        ConsoleHandler logHandler = new ConsoleHandler();
        Level logLevel = Level.WARNING;
        String logFormat = "[ %4$s ] %5$s%6$s%n";

        if (isDebug) {
            logFormat = "%1$tF %1$tT %2$s - %4$s: %5$s%6$s%n";
            logLevel = Level.FINER;
        }
        System.setProperty("java.util.logging.SimpleFormatter.format", logFormat);
        logger.setLevel(logLevel);
        logHandler.setLevel(logLevel);
        logHandler.setFormatter(new SimpleFormatter());
        logger.addHandler(logHandler);
        logger.setUseParentHandlers(false);
    }

    private static HomedConfig setupConfig(String confDir) {
        config = new Config(confDir);
        config.resisterConfigType("homed", new ConfigType<HomedConfig>(HomedConfig.class));
        HomedConfig homedConfig = (HomedConfig) config.get("homed");
        return homedConfig;
    }
}
