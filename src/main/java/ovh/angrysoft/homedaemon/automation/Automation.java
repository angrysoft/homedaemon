package ovh.angrysoft.homedaemon.automation;

import java.util.List;
import java.util.Objects;

import ovh.angrysoft.homedaemon.automation.actions.Action;
import ovh.angrysoft.homedaemon.automation.conditions.Condition;

public class Automation implements Runnable {
    protected boolean running = false;
    protected String sid;
    protected List<Action> actions;
    protected List<Action> actionsFalse;
    protected List<Condition> conditions;

    public Automation(String sid, List<Condition> conditions, List<Action> actions,
            List<Action> actionsFalse) {
        this.sid = sid;
        this.actions = actions;
        this.actionsFalse = actionsFalse;
        this.conditions = conditions;
    }

    public String getSid() {
        return sid;
    }

    public void run() {
        if (running)
            return;
        running = true;
        List<Action> actionsToRun = this.actions;

        if (!checkCondition()) {
            actionsToRun = this.actionsFalse;
        }

        for (Action action : actionsToRun) {
            action.run();
        }
        running = false;
    }

    private boolean checkCondition() {
        for (Condition condition : conditions) {
            if (!condition.check()) {
                return false;
            }
        }
        return true;
    }

    public boolean isRunning() {
        return running;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(getSid());
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Automation))
            return false;
        Automation auto = (Automation) o;
        return this.sid.equals(auto.getSid());
    }
}
