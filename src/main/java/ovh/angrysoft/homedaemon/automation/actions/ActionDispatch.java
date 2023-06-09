package ovh.angrysoft.homedaemon.automation.actions;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;

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
        bus.dispatch(Event.actionEvent(eventName, eventValue));
    }
}
