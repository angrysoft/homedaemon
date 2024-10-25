package ovh.angrysoft.homedaemon.bus;

import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

public class Topic {
    private List<String> topicParts;
    private boolean wildCard = false;

    private Topic(String[] topicArray) {
        this.topicParts = new ArrayList<>();
        for (String part : topicArray) {
            if (!part.isEmpty())
                this.topicParts.add(part);
        }
        if (this.topicParts.contains("*"))
            this.wildCard = true;
    }

    public static Topic fromString(String topicString) {
        return new Topic(topicString.split("\\."));
    }

    public static Topic fromArray(String[] topicArray) {
        return new Topic(topicArray);
    }

    public static Topic newTimeTopic(LocalTime time) {
        return new Topic(new String[] { "time",
                String.format("%02d:%02d:%02d", time.getHour(), time.getMinute(), time.getSecond()) });
    }

    public List<String> getTopicParts() {
        return topicParts;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Topic)) {
            return false;
        }
        List<String> topicPartsToCompare = ((Topic) o).getTopicParts();

        if (!this.wildCard)
            return topicParts.equals(topicPartsToCompare);

        int maxLoop = Math.min(this.topicParts.size(), topicPartsToCompare.size());
        for (int i = 0; i < maxLoop; i++) {
            if (this.topicParts.get(i).equals("*"))
                break;
            if (!this.topicParts.get(i).equals(topicPartsToCompare.get(i)))
                return false;
        }
        return true;
    }

    @Override
    public int hashCode() {
        return this.topicParts.hashCode();
    }

    @Override
    public String toString() {
        return String.join(".", topicParts);
    }
}
