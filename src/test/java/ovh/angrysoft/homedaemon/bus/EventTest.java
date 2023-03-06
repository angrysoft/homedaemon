package ovh.angrysoft.homedaemon.bus;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class EventTest {
    @Test
    @DisplayName("Testing event")
    public void testGetTopicList() {
        Event event = new Event("one.two.three", "some payload");
        String[] topicList = {"one", "two", "three"};
        assertTrue(Arrays.equals(topicList, event.getTopicList()));
    }
    
    @Test
    @DisplayName("Testing event")
    public void testGetPayload() {
        Event event = new Event("one.two.three", "some payload");
        String s = "some payload";
        assertEquals(s, (String) event.getPayload());
    }
    
}
