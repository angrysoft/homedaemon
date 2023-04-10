package ovh.angrysoft.homedaemon.bus.Events;

public class ActionEvent extends DeviceEvent {

    public ActionEvent(String name, Object value) {
        super("Action", name, value);
        this.topicList = new String[] { "action", name, value.toString() };
    }
}
