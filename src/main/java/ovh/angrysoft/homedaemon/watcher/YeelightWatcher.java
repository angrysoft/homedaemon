package ovh.angrysoft.homedaemon.watcher;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.connections.TcpConnection;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

class YeelightNotification {
    private String method;
    private HashMap<String, Object> params;

    public String getMethod() {
        return method;
    }

    public Map<String, Object> getParams() {
        return params;
    }

    public String toString() {
        return String.format("%s - %s", method, params);
    }
}


public class YeelightWatcher extends Watcher {
    private String ip;
    private int port;
    private Gson json = new Gson();

    public YeelightWatcher(String sid, String ip, int port) {
        super(sid);
        this.ip = ip;
        this.port = port;
    }

    @Override
    public void run() {

        try (TcpConnection conn = new TcpConnection(ip, port)) {
            while (true) {
                parseData(conn.recv());
                // YeelightNotification notify = new Gson().fromJson(rec, YeelightNotification.class);
                // Map<String, Object> params = notify.getParams();
                // params.forEach((k, v) -> {
                //     String name = k;
                //     Object value;
                //     switch (k) {
                //         case "power":
                //             name = "state";
                //             value = (String) v;
                //             break;
                //         case "bright":
                //         case "ct":
                //         case "rgb":
                //         case "hue":
                //         case "sat":
                //         case "color_mode":
                //         case "flowing":
                //         case "delayoff":
                //             Double tmp = (double) v;
                //             value = tmp.intValue();
                //             break;
                //         default:
                //             value = v;
                //     }
                //     handler.call(Event.statusEvent(sid, name, value));
                // });
            }
        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }

    private void parseData(String data) {

        JsonObject yeelightNotify = json.fromJson(data, JsonObject.class);
        for (Entry<String, JsonElement> entry : yeelightNotify.entrySet()) {
            Object value = null;
            JsonElement element = entry.getValue();
            String key = entry.getKey();
            String name = key;
            switch (key) {
                case "power":
                    name = "state";
                    value = element.getAsString();
                    break;
                case "bright":
                case "ct":
                case "rgb":
                case "hue":
                case "sat":
                case "color_mode":
                case "flowing":
                case "delayoff":
                    value = element.getAsInt();
                    break;
                default:
                    value = element.getAsString();
            }
            handler.call(Event.statusEvent(sid, name, value));
        }
    }

}
