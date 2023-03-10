package ovh.angrysoft.homedaemon.bus;

public class Trigger {
    private Handler handler;
    private String[] topicList;
    private boolean wildCard;

    public Trigger(String topic, Handler handler) {
        topicList = topic.split("\\.");
        this.handler = handler;
        this.wildCard = false;
        for (String subTopic : topicList) {
            if (subTopic.equals("*"))
                this.wildCard = true;
        }
    }

    public boolean compareTopic(String[] topicList) {
        if (!this.wildCard && topicList.length != this.topicList.length)
            return false;
        int maxLoop = Math.min(this.topicList.length, topicList.length);
        for (int i = 0; i < maxLoop; i++) {
            if (this.topicList[i].equals("*"))
                break;
            if (! this.topicList[i].equals(topicList[i]))
                return false;
        }
        return true;
    }

    public void call(Event event) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                handler.call(event);
            }
        }).start();
    }
}
