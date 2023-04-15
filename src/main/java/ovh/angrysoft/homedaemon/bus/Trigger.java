package ovh.angrysoft.homedaemon.bus;

public class Trigger {
    private Handler handler;
    private String[] topicList;
    private boolean wildCard;
    private boolean oneShot;
    private String id = "";

    public Trigger(String topic, Handler handler) {
        this(topic, handler, false);
    }

    public Trigger(String topic, Handler handler, boolean oneShot) {
        this.oneShot = oneShot;
        topicList = topic.split("\\.");
        this.handler = handler;
        this.wildCard = false;
        for (String subTopic : topicList) {
            if (subTopic.equals("*"))
                this.wildCard = true;
        }
    }

    // TODO seperate class topic topic.equals
    public boolean compareTopic(String[] topicList) {
        if (!this.wildCard && topicList.length != this.topicList.length)
            return false;
        int maxLoop = Math.min(this.topicList.length, topicList.length);
        for (int i = 0; i < maxLoop; i++) {
            if (this.topicList[i].equals("*"))
                break;
            if (!this.topicList[i].equals(topicList[i]))
                return false;
        }
        return true;
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
