package ovh.angrysoft.homedaemon.automation;

public class AutomationFactory {
    public Automation getAutomation(AutomationInfo info) {
        switch(info.getType()) {
            case "actionHandler":
                return new ActionHandler(info);
            case "script":

        }
        return null;
    }
}
