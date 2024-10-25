package ovh.angrysoft.homedaemon.watcher;

import java.io.IOException;
import java.net.InetAddress;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import javax.jmdns.JmDNS;
import javax.jmdns.ServiceEvent;
import javax.jmdns.ServiceInfo;
import javax.jmdns.ServiceListener;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.annotations.SerializedName;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.connections.ewelink.AuthUtils;

public final class EwelinkWatcher extends Watcher {
    private static EwelinkWatcher instance;
    private static Map<String, String> watchedDevices = new HashMap<>();

    private EwelinkWatcher() {
        super("MdnsWatcher");
    }

    public static synchronized EwelinkWatcher getInstance() {
        if (instance != null)
            return instance;
        return new EwelinkWatcher();
    }

    @Override
    public void run() {
        try (JmDNS jmDNS = JmDNS.create(InetAddress.getLocalHost())) {
            jmDNS.addServiceListener("_ewelink._tcp.local.",
                    new WatcherListener(watchedDevices, handler));
            while (true) {
                Thread.sleep(100);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static synchronized void registerDevice(String sid) {
        watchedDevices.put(sid, "");
    }


    public static synchronized void registerDevice(String sid, String token) {
        watchedDevices.put(sid, token);
    }


}


class WatcherListener implements ServiceListener {
    WatcherHandler handler;
    private Map<String, String> watchedDevice;
    private Gson json = new Gson();

    public WatcherListener(Map<String, String> watchedDevice, WatcherHandler handler) {
        this.watchedDevice = watchedDevice;
        this.handler = handler;
    }

    @Override
    public void serviceAdded(ServiceEvent event) {
        // there are no interesting information listen for serviceResoled.
    }

    @Override
    public void serviceRemoved(ServiceEvent event) {
        // there are no interesting information listen for serviceResoled.
    }

    @Override
    public void serviceResolved(ServiceEvent event) {
        Map<String, Object> devInfo = new HashMap<>();
        ServiceInfo info = event.getInfo();
        Iterator<String> propertyNames = info.getPropertyNames().asIterator();
        while (propertyNames.hasNext()) {
            String name = propertyNames.next();
            devInfo.put(name, info.getPropertyString(name));
        }
        parseData(devInfo);

    }

    private void parseData(Map<String, Object> devInfo) {
        String sid = (String) devInfo.get("id");
        if (sid == null || sid.isEmpty() || !watchedDevice.containsKey(sid)) {
            return;
        }
        StringBuilder dataBuilder = new StringBuilder();
        for (int i = 1; i < 5; i++) {
            if (devInfo.containsKey("data" + i)) {
                dataBuilder.append(devInfo.get("data" + i));
            } else {
                break;
            }

        }
        String data = dataBuilder.toString();

        if (devInfo.containsKey("encrypt") && devInfo.get("encrypt").equals("true")) {
            data = AuthUtils.decryptData(data, watchedDevice.get(devInfo.get("id")),
                    (String) devInfo.get("iv"));
        }

        JsonObject ewelinkNotify = json.fromJson(data, JsonObject.class);
        for (Entry<String, JsonElement> entry : ewelinkNotify.entrySet()) {
            Object value = null;
            JsonElement element = entry.getValue();
            String key = entry.getKey();
            String name = key;
            switch (key) {
                case "switches":
                    element.getAsJsonArray().forEach(switchState -> {
                        JsonObject switchInfo = switchState.getAsJsonObject();
                        String outlet = "outlet" + switchInfo.get("outlet");
                        String state = switchInfo.get("switch").getAsString();
                        handler.call(Event.statusEvent(sid, outlet, state));
                    });
                    continue;
                case "switch":
                    name = "outlet";
                    value = element.getAsString();
                    break;
                case "lightMode":
                    name = "ambientLightScene";
                    value = element.getAsInt();
                    break;

                case "lightSwitch":
                    name = "ambientLight";
                    value = element.getAsString();
                    break;
                default:
                    value = element.getAsString();
                    break;
            }
            handler.call(Event.statusEvent(sid, name, value));
        }
    }

}


record EwelinkNotify(int percentageControl, boolean calibState, String fwVersion, int rssi,
        String ssid, String bssid, List<SwitchState> switches, String lightSwitch) {
}


record SwitchState(@SerializedName("switch") String switchState, int outlet) {
}
