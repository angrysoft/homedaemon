package ovh.angrysoft.homedaemon.bus.Events;

import java.util.HashMap;

import ovh.angrysoft.homedaemon.bus.Event;

public abstract class DeviceEvent implements Event{
    protected String sid;
    protected String name;
    protected Object value;
    protected String[] topicList;

    public DeviceEvent(String sid, String name, Object value) {
        this.sid = sid;
        this.name = name;
        this.value = value;
    }

    public String getSid() {
        return sid;
    }

    public String getName() {
        return name;
    }

    public Object getValue() {
        return value;
    }

    public String toString() {
        return String.join(".", topicList);
    }

    public HashMap<String, Object> getPayload() {
        HashMap<String, Object> payload = new HashMap<String, Object>();
        payload.put(name, value);
        return payload;
    }

    public String[] getTopicList() {
        return this.topicList;
    }
}
