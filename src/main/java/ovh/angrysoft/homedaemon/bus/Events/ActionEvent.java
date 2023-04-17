package ovh.angrysoft.homedaemon.bus.Events;

import ovh.angrysoft.homedaemon.bus.Topic;

public class ActionEvent extends DeviceEvent {

    public ActionEvent(String name, Object value) {
        super("Action", name, value);
        this.topic = Topic.fromArray(new String[] { "action", name, value.toString() });
    }
}
