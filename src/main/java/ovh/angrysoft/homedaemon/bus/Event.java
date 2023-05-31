package ovh.angrysoft.homedaemon.bus;

import java.util.HashMap;

public interface Event {

    public HashMap<String, Object> getPayload();

    public Topic getTopic();

    public String toJson();
}
