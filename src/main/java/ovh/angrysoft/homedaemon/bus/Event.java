package ovh.angrysoft.homedaemon.bus;

public class Event {
    private String[] topicList;
    private Object payload;

    public Event(String topic, Object payload) {
        this.topicList = topic.split("\\.");
        this.payload = payload;
    }

    public Object getPayload() {
        return payload;
    }

    public String[] getTopicList() {
        return topicList;
    }
}
