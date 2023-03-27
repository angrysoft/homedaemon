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
import com.google.gson.JsonIOException;
import com.google.gson.JsonSyntaxException;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Trigger;

public class AutomationManager {
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");
    private AutomationParser automationParser;
    private EventBus bus;
    private String automationDirPath;
    private Set<Automation> automations;

    public AutomationManager(String automationDirPath, EventBus bus) {
        this.automationParser = new AutomationParser();
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
                
                AutomationInfo automationInfo = new Gson().fromJson(new FileReader(automationInfoFile),
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

    private synchronized void registerAutomation(String triggerString, Automation automation) {
        this.automations.add(automation);
        Trigger automationTrigger = new Trigger(triggerString, (Event event) ->{
            LOGGER.info(String.format("automation: %s - action", Arrays.toString(event.getTopicList())));
        });
        this.bus.addTrigger(automationTrigger);
    }
}
