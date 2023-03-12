package ovh.angrysoft.homedaemon.bus.Events;

public class StatusEvent extends DeviceEvent {

    public StatusEvent(String sid, String name, Object value) {
        super(sid, name, value);
        this.topicList = new String[] { "status", sid, name, value.toString() };
    }
}
