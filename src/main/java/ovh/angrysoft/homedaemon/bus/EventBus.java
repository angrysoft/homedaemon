package ovh.angrysoft.homedaemon.bus;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class EventBus {
    private HashMap<String, Trigger> triggers;
    private ThreadPoolExecutor triggerExecutor;

    public EventBus() {
        this.triggers = new HashMap<>();
        this.triggerExecutor = (ThreadPoolExecutor) Executors.newCachedThreadPool();
    }

    public synchronized int triggersSize() {
        return triggers.size();
    }

    public synchronized String addTrigger(Trigger trigger) {
        String id = UUID.randomUUID().toString();
        if (triggers.containsKey(id)) {
            return addTrigger(trigger);
        }
        triggers.put(id, trigger);
        trigger.setId(id);
        return id;
    }

    public synchronized void delTrigger(String id) {
        if (triggers.containsKey(id)) {
            triggers.remove(id);
        }
    }

    public void dispatch(Event event) {
        for (Map.Entry<String, Trigger> entry : triggers.entrySet()) {
            triggerExecutor.submit(() -> {
                Trigger trigger = entry.getValue();
                if (trigger.compareTopic(event.getTopicList())) {
                    trigger.call(event);
                    if (trigger.isOneShot())
                        delTrigger(trigger.getId());
                }
            });
        }
    }
}
