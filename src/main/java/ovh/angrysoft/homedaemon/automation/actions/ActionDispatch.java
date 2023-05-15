package ovh.angrysoft.homedaemon.automation.actions;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Events.ActionEvent;

public class ActionDispatch extends Action {
    private EventBus bus;
    private String eventName;
    private Object eventValue;

    public ActionDispatch(String eventName, Object eventValue, EventBus bus) {
        this.bus = bus;
        this.eventName = eventName;
        this.eventValue = eventValue;
    }

    @Override
    public void run() {
        bus.dispatch(new ActionEvent(eventName, eventValue));
    }
}
