package ovh.angrysoft.homedaemon.bus;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class EventBusTest {
    @Test
    @DisplayName("Test Event bus addTrigger")
    public void testAddTrigger() {
        Trigger trigger = new Trigger("report.123341421.status.off", (Event event) -> {
            System.out.println((String) event.getPayload());
        });

        EventBus bus = new EventBus();
        bus.addTrigger(trigger);
        assertEquals(bus.triggersSize(), 1);
    }

    @Test
    @DisplayName("Test Event bus addTrigger")
    public void testDelTrigger() {
        Trigger trigger = new Trigger("report.123341421.status.off", (Event event) -> {
            System.out.println((String) event.getPayload());
        });

        EventBus bus = new EventBus();
        String id = bus.addTrigger(trigger);
        bus.delTrigger(id);
        assertEquals(bus.triggersSize(), 0);
    }

    @Test
    @DisplayName("Test Event bus addTrigger")
    public void testDispatch() {
        List<String> status = new ArrayList<>();
        Trigger trigger = new Trigger("report.123341421.status.off", (Event event) -> {
            status.add((String) event.getPayload());
        });

        EventBus bus = new EventBus();
        bus.addTrigger(trigger);
        bus.dispatch(new Event("report.123341421.status.off", "off"));
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        assertEquals(status.get(0), "off");
    }

    @Test
    @DisplayName("Test Event bus addTrigger")
    public void testDispatchWildcard() {
        List<String> status = new ArrayList<>();
        Trigger trigger = new Trigger("report.*", (Event event) -> {
            status.add((String) event.getPayload());
        });

        EventBus bus = new EventBus();
        bus.addTrigger(trigger);
        bus.dispatch(new Event("report.123341421.status.off", "WildCard"));
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        assertEquals(status.get(0), "WildCard");
    }
}
