package ovh.angrysoft.homedaemon.bus;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class TopicTest {
    @Test
    public void compareTopicTrue() {
        Topic one = Topic.fromString("status.123341421.status.off");
        Topic two = Topic.fromString("status.123341421.status.off");
        assertTrue(one.equals(two));
    }

    @Test
    public void compareTopicFromArrayTrue() {
        Topic one = Topic.fromArray(new String[] {"status", "123341421", "status", "off"});
        Topic two = Topic.fromArray(new String[] {"status", "123341421", "status", "off"});
        assertTrue(one.equals(two));
    }

    @Test
    public void compareTopicFromArrayFalse() {
        Topic one = Topic.fromArray(new String[] {"status", "123341421", "status", "off"});
        Topic two = Topic.fromArray(new String[] {"status", "123341421", "status", "on"});
        assertFalse(one.equals(two));
    }

    @Test
    public void compareTopicFromArrayToFromStringFalse() {
        Topic one = Topic.fromArray(new String[] {"status", "123341421", "status", "off"});
        Topic two = Topic.fromString("status.123341421.status.on");
        assertFalse(one.equals(two));
    }

    @Test
    public void compareTopicFromArrayToFromStringTrue() {
        Topic one = Topic.fromArray(new String[] {"status", "123341421", "status", "off"});
        Topic two = Topic.fromString("status.123341421.status.off");
        assertTrue(one.equals(two));
    }


    @Test
    public void compareTopicFalse() {
        Topic one = Topic.fromString("status.123341421.status.off");
        Topic two = Topic.fromString("status.123341421.power.on");
        assertFalse(one.equals(two));
    }

    @Test
    public void testCompareTopicWildCard() {
        Topic one = Topic.fromString("status.123341421.*");
        Topic two = Topic.fromString("status.123341421.status.off");
        Topic three = Topic.fromString("status.123341421.power.off");

        assertTrue(one.equals(two));
        assertTrue(one.equals(three));
    }
}
