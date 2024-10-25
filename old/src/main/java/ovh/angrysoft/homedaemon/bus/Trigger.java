package ovh.angrysoft.homedaemon.bus;

public class Trigger {
    private Handler handler;
    private boolean oneShot;
    private String id = "";
    private Topic topic;

    public Trigger(Topic topic, Handler handler) {
        this(topic, handler, false);
    }

    public Trigger(Topic topic, Handler handler, boolean oneShot) {
        this.oneShot = oneShot;
        this.topic = topic;
        this.handler = handler;
    }

    public boolean compareTopic(Topic topic) {
        return this.topic.equals(topic);
    }

    public void call(Event event) {
        handler.call(event);
    }

    public boolean isOneShot() {
        return oneShot;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
