package ovh.angrysoft.homedaemon.bus.Events;

import ovh.angrysoft.homedaemon.bus.Topic;

public class CustomEvent extends DeviceEvent {

    public CustomEvent(String sid, String eventName, String name, Object value) {
        super(sid, name, value);
        this.topic = Topic.fromArray(new String[] { eventName, sid, name, value.toString() });

    }
    
}
