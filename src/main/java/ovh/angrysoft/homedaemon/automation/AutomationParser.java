package ovh.angrysoft.homedaemon.automation;

import java.util.ArrayList;
import java.util.List;

import ovh.angrysoft.homedaemon.automation.actions.Action;
import ovh.angrysoft.homedaemon.automation.actions.ActionExecute;
import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class AutomationParser {
    private DeviceManager deviceManager;

    public AutomationParser(DeviceManager deviceManager) {
        this.deviceManager = deviceManager;
    }

    public Automation parse(AutomationInfo info) {
        System.out.println(info.getSid());
        System.out.println(info.getTrigger());
        List<Action> actions = this.parseActions(info.getActions());
        return new Automation(false, info.getSid(), actions);
    }

    private List<Action> parseActions(List<ActionInfo> actions) {
        List<Action> result = new ArrayList<>();
        for (ActionInfo actionInfo : actions) {
            System.out.println(actionInfo);
            result.add(this.parseAction(actionInfo));
        }
        return result;
    }

    private Action parseAction(ActionInfo action) {
        switch (action.getType()) {
            case "execute":
                return new ActionExecute(action.getSid(), action.getCmd(), action.getArg(), action.isRunInBackground(),
                        deviceManager);
        }
        return null;
    }
}
