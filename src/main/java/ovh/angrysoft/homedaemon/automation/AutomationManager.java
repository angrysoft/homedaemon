package ovh.angrysoft.homedaemon.automation;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonIOException;
import com.google.gson.JsonSyntaxException;
import com.google.gson.ToNumberPolicy;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Trigger;
import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class AutomationManager {
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");
    private AutomationParser automationParser;
    private EventBus bus;
    private DeviceManager deviceManager;
    private String automationDirPath;
    private Set<Automation> automations;

    public AutomationManager(String automationDirPath, EventBus bus, DeviceManager deviceManager) {
        this.deviceManager = deviceManager;
        this.automationParser = new AutomationParser(this.deviceManager);
        this.bus = bus;
        this.automationDirPath = automationDirPath;
        this.automations = new HashSet<>();
    }

    public void loadAutomation() {
        File automationDir = new File(automationDirPath);
        LOGGER.info(automationDirPath);
        if (!automationDir.exists() || !automationDir.isDirectory()) {
            LOGGER.severe("Cannot access device dir : " + automationDirPath);
            return;
        }

        for (File automationInfoFile : automationDir.listFiles()) {
            if (!automationInfoFile.getName().endsWith(".json"))
                continue;

            try {
                Gson gson = new GsonBuilder().setObjectToNumberStrategy(ToNumberPolicy.LAZILY_PARSED_NUMBER).create();

                AutomationInfo automationInfo = gson.fromJson(new FileReader(automationInfoFile),
                        AutomationInfo.class);
                automationInfo.checkFields();

                LOGGER.log(Level.INFO, "load automation: {0}", automationInfo.getSid());

                Automation automation = automationParser.parse(automationInfo);
                this.registerAutomation(automationInfo.getTrigger(), automation);
            } catch (JsonSyntaxException | JsonIOException | FileNotFoundException e) {
                LOGGER.severe(String.format("%s - %s", automationInfoFile.getName(), e.getMessage()));
            }
        }
    }

    private void registerAutomation(String triggerString, Automation automation) {
        synchronized (this) {
            this.automations.add(automation);
        }
        Trigger automationTrigger = new Trigger(triggerString, (Event event) -> {
            LOGGER.info(String.format("automation: %s - action", Arrays.toString(event.getTopicList())));
            // TODO ThreadPool
            new Thread(automation).start();
        });
        this.bus.addTrigger(automationTrigger);
    }
}
