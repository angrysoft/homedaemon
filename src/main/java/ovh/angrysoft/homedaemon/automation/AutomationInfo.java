package ovh.angrysoft.homedaemon.automation;

import java.util.List;
import java.util.Map;

public class AutomationInfo {
    private String sid;
    private String type;
    private String trigger;
    private Map<String, String> name;
    private List<ConditionInfo> conditions;
    private List<ActionInfo> actions;
    private List<ActionInfo> actionsFalse;
    private List<State> state;

    public AutomationInfo(String sid, String type, String trigger, Map<String, String> name,
            List<ConditionInfo> conditions, List<ActionInfo> actions, List<ActionInfo> actionsFalse,
            List<State> state) {
        this.sid = sid;
        this.type = type;
        this.trigger = trigger;
        this.name = name;
        this.conditions = conditions;
        this.actions = actions;
        this.actionsFalse = actionsFalse;
        this.state = state;
    }

    public String getSid() {
        return sid;
    }

    public String getType() {
        return type;
    }

    public String getTrigger() {
        return trigger;
    }

    public Map<String, String> getName() {
        return name;
    }

    public List<ConditionInfo> getConditions() {
        return conditions;
    }

    public List<ActionInfo> getActions() {
        return actions;
    }

    public List<ActionInfo> getActionsFalse() {
        return actionsFalse;
    }

    public List<State> getState() {
        return state;
    }

    public void checkFields() throws VerifyError {
        if (sid == null)
            throw new VerifyError("sid is null");

        if (type == null)
            throw new VerifyError("type is null");

        if (trigger == null)
            throw new VerifyError("trigger is null");

        if (name == null)
            throw new VerifyError("name is null");

        if (actions == null)
            throw new VerifyError("actions is null");

        if (actionsFalse == null)
            throw new VerifyError("actionsFalse is null");

        if (conditions == null)
            throw new VerifyError("conditions is null");
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("sid = ")
                .append(sid)
                .append("\n");

        sb.append("trigger = ")
                .append(trigger)
                .append("\n");
        sb.append("... ")
                .append(conditions)
                .append(actions);
        return sb.toString();
    }

}

class State {
    String attrName;
    String attrType;
    Object attrValue;
}

class ConditionInfo {
    String type;
    List<TestCaseInfo> testCases;

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("type: ")
                .append(type);

        sb.append("TestCases: ")
                .append(testCases);
        return sb.toString();
    }
}

class TestCaseInfo {
    String type;
    String sid;
    String attrName;
    Object attrValue;
}

class ActionInfo {
    private String type;
    private String sid;
    private String cmd;
    private Object arg;
    private boolean runInBackground;

    /**
     * @param type
     * @param sid
     * @param cmd
     * @param arg
     * @param runInBackground
     */
    public ActionInfo(String type, String sid, String cmd, Object arg, boolean runInBackground) {
        this.type = type;
        this.sid = sid;
        this.cmd = cmd;
        this.arg = arg;
        this.runInBackground = runInBackground;
    }

    public String getType() {
        return type;
    }

    public String getSid() {
        return sid;
    }

    public String getCmd() {
        return cmd;
    }

    public Object getArg() {
        return arg;
    }

    public boolean isRunInBackground() {
        return runInBackground;
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        if (this.type != null)
            result.append(this.type.toString())
                    .append(", ");
        if (this.sid != null)
            result.append(this.sid.toString())
                    .append(", ");
        if (this.cmd != null)
            result.append(this.cmd.toString())
                    .append(", ");
        if (this.arg != null)
            result.append(this.arg.toString())
                    .append(", ");
        return result.toString();
    }

}
