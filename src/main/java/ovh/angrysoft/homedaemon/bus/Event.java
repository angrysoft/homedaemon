package ovh.angrysoft.homedaemon.bus;

import java.util.HashMap;

import com.google.gson.Gson;

public class Event {

    protected String sid;
    protected String name;
    protected Object value;
    protected String eventName;
    protected Topic topic;

    private Event(String eventName, String sid, String name, Object value) {
        this.sid = sid;
        this.name = name;
        this.value = value;
        this.eventName = eventName;
        String[] topicArray;
        if (this.value == null) {
            topicArray = new String[] { eventName, sid, name };
        } else {
            topicArray = new String[] { eventName, sid, name, this.value.toString() };
        }
        this.topic = Topic.fromArray(topicArray);
    }

    public static Event statusEvent(String sid, String name, Object value) {
        return new Event("status", sid, name, value);
    }

    public static Event timeEvent(String name, String value) {
        return new Event("tick", "clock", name, value);
    }

    public static Event executeEvent(String sid, String cmd, Object arg) {
        return new Event("execute", sid, cmd, arg);
    }

    public static Event actionEvent(String actionName, Object actionValue) {
        return new Event("action", "automation", actionName, actionValue);
    }

    public static Event customEvent(String eventName, String sid, String name, Object value) {
        return new Event(eventName, sid, name, value);
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
