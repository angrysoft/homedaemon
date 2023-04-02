package ovh.angrysoft.homedaemon.automation;

import java.util.List;
import java.util.Objects;

import ovh.angrysoft.homedaemon.automation.actions.Action;
import ovh.angrysoft.homedaemon.automation.conditions.Condition;

public class Automation implements Runnable {
    protected boolean running = false;
    protected String sid;
    protected List<Action> actions;
    protected List<Condition> conditions;

    public Automation(boolean running, String sid, List<Action> actions, List<Condition> conditions) {
        this.running = running;
        this.sid = sid;
        this.actions = actions;
        this.conditions = conditions;
    }

    public String getSid() {
        return sid;
    }

    public void run() {
        if (running)
            return;
        running = true;
        for (Condition condition : conditions) {
            if (!condition.check())
                return;
        }

        for (Action action : actions) {
            action.run();
        }
        running = false;
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
