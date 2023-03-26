package ovh.angrysoft.homedaemon.automation;

import java.util.Objects;

public abstract class Automation {
    protected boolean running = false;
    protected String sid;
    
    public String getSid() {
        return sid;
    }

    public abstract void run();

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
