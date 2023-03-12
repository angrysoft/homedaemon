package ovh.angrysoft.homedaemon.bus.Events;

public class ExecuteEvent extends DeviceEvent {

    public ExecuteEvent(String sid, String name, Object value) {
        super(sid, name, value);
        this.topicList = new String[] { "execute", sid, name, value.toString() };
    }
}
