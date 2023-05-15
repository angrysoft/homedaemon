package ovh.angrysoft.homedaemon.bus.Events;

import ovh.angrysoft.homedaemon.bus.Topic;

public class StatusEvent extends DeviceEvent {

    public StatusEvent(String sid, String name, Object value) {
        super(sid, name, value);
        this.topic = Topic.fromArray(new String[] { "status", sid, name, value.toString() });
    }
}
