package ovh.angrysoft.homedaemon.bus;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;

public class EventTest {
    @Test
    @DisplayName("Testing event")
    public void testGetTopicList() {
        Event event = new StatusEvent("11223344", "key", "value");
        String[] topicList = {"status", "11223344", "key", "value"};
        assertTrue(Arrays.equals(topicList, event.getTopicList()));
    }
    
    @Test
    @DisplayName("Testing event")
    public void testGetPayload() {
        Event event = new StatusEvent("11223344", "key", "some payload");
        String s = "some payload";
        assertEquals(s, (String) event.getPayload().get("key"));
    }
    
}
