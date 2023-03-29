package ovh.angrysoft.homedaemon.automation;

import java.util.List;
import java.util.Map;

public class AutomationInfo {
    private String sid;
    private String type;
    private String trigger;
    private Map<String, String> name;
    private Map<String, Condition> conditions;
    private Map<String, Action> actions;

    public AutomationInfo(String sid, String type, String trigger, Map<String, String> name,
            Map<String, Condition> conditions, Map<String, Action> actions) {
        this.sid = sid;
        this.type = type;
        this.trigger = trigger;
        this.name = name;
        this.conditions = conditions;
        this.actions = actions;
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

    public Map<String, Condition> getConditions() {
        return conditions;
    }

    public Map<String, Action> getActions() {
        return actions;
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
        return sb.toString();
    }
}

class Condition {
}

class Actions {
    private List<Action> parallel;
    private List<Action> serial;
    private Action execute;
    private Action script;

    public Actions(List<Action> parallel, List<Action> serial, Action execute, Action script) {
        this.parallel = parallel;
        this.serial = serial;
        this.execute = execute;
        this.script = script;
    }

    public List<Action> getParallel() {
        return parallel;
    }

    public List<Action> getSerial() {
        return serial;
    }

    public Action getExecute() {
        return execute;
    }

    public Action getScript() {
        return script;
    }
}


class Action {
    private String type;
    private String sid;
    private String cmd;
    private Object args;

    public Action(String type, String sid, String cmd, Object args) {
        this.type = type;
        this.sid = sid;
        this.cmd = cmd;
        this.args = args;
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

    public Object getArgs() {
        return args;
    }

}
