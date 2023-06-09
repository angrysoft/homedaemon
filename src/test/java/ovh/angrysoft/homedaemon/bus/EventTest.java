package ovh.angrysoft.homedaemon.bus;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class EventTest {
    @Test
    @DisplayName("Testing event")
    public void testGetTopicList() {
        Event event = Event.statusEvent("11223344", "key", "value");
        Topic topic = Topic.fromString("status.11223344.key.value");
        assertTrue(topic.equals(event.getTopic()));
    }
    
    @Test
    @DisplayName("Testing event")
    public void testGetPayload() {
        Event event = Event.statusEvent("11223344", "key", "some payload");
        String s = "some payload";
        assertEquals(s, (String) event.getPayload().get("key"));
    }
    
}
