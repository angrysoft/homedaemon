package ovh.angrysoft.homedaemon.automation.actions;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;

public class ActionState extends Action {
    private EventBus bus;
    private String attrName;
    private Object attrValue;

    public ActionState(String attrName, Object attrValue, EventBus bus) {
        this.bus = bus;
        this.attrName = attrName;
        this.attrValue = attrValue;
    }

    @Override
    public void run() {
        System.err.println("state." + attrName + "." + attrValue);
        bus.dispatch(new StatusEvent("state", attrName, attrValue));
    }
}
