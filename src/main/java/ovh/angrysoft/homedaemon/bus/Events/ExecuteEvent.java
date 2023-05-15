package ovh.angrysoft.homedaemon.bus.Events;

import ovh.angrysoft.homedaemon.bus.Topic;

public class ExecuteEvent extends DeviceEvent {

    public ExecuteEvent(String sid, String name, Object value) {
        super(sid, name, value);
        this.topic = Topic.fromArray(new String[] { "execute", sid, name, value.toString() });
    }
}
