package ovh.angrysoft.homedaemon.bus.Events;

import ovh.angrysoft.homedaemon.bus.Topic;

public class TimeEvent extends DeviceEvent {

    public TimeEvent(String sid, String name, Object value) {
        super(sid, name, value);
        this.topic = Topic.fromArray(new String[] { sid, name, value.toString() });
    }
}
