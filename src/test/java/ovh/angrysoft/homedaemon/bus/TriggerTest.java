package ovh.angrysoft.homedaemon.bus;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class TriggerTest {
    @Test
    @DisplayName("Trigger compare test")
    public void testCompareTopic() {
        Trigger trigger = new Trigger("report.123341421.status.off", (Event event) -> {
            System.out.println((String) event.getPayload());
        });
        String[] topicList = "report.123341421.status.off".split("\\.");
        assertTrue(trigger.compareTopic(topicList));
    }

    @Test
    @DisplayName("Trigger compare test")
    public void testCompareTopicWildCard() {
        Trigger trigger = new Trigger("report.*", (Event event) -> {
            System.out.println((String) event.getPayload());
        });
        String[] topicList = "report.123341421.status.off".split("\\.");
        assertTrue(trigger.compareTopic(topicList));
    }
}
