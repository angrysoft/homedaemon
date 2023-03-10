package ovh.angrysoft.homedaemon.watcher;

public class StatusMessage {
    private String sid;
    private String name;
    private Object value;

    public StatusMessage(String sid, String name, Object value) {
        this.sid = sid;
        this.name = name;
        this.value = value;
    }

    public String getSid() {
        return sid;
    }

    public String getName() {
        return name;
    }

    public Object getValue() {
        return value;
    }

    public String toString() {
        return String.format("status.%s.%s.%s", sid, name, value);
    }
}
