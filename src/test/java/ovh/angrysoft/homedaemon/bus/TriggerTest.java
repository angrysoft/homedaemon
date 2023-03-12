package ovh.angrysoft.homedaemon.bus;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class TriggerTest {
    @Test
    @DisplayName("Trigger compare test")
    public void testCompareTopic() {
        Trigger trigger = new Trigger("status.123341421.status.off", (Event event) -> {
            System.out.println((String) event.getPayload().get("status"));
        });
        String[] topicList = "status.123341421.status.off".split("\\.");
        assertTrue(trigger.compareTopic(topicList));
    }

    @Test
    @DisplayName("Trigger compare test")
    public void testCompareTopicWildCard() {
        Trigger trigger = new Trigger("status.*", (Event event) -> {
            System.out.println((String) event.getPayload().get("status"));
        });
        String[] topicList = "status.123341421.status.off".split("\\.");
        assertTrue(trigger.compareTopic(topicList));
    }
}
