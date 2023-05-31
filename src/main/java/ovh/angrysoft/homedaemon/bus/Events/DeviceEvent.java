package ovh.angrysoft.homedaemon.bus.Events;

import java.util.HashMap;

import com.google.gson.Gson;

import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.Topic;

public abstract class DeviceEvent implements Event {
    protected String sid;
    protected String name;
    protected Object value;
    protected Topic topic;

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
        return topic.toString();
    }

    public HashMap<String, Object> getPayload() {
        HashMap<String, Object> payload = new HashMap<String, Object>();
        payload.put(name, value);
        return payload;
    }

    public Topic getTopic() {
        return topic;
    }

    public String toJson() {
        HashMap<String, Object> data = new HashMap<String, Object>();
        data.put("sid", this.sid);
        data.put("payload", getPayload());
        Gson gson = new Gson();
        return gson.toJson(data);
    }
}
