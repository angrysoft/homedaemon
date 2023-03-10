package ovh.angrysoft.homedaemon.watcher;

import java.util.HashMap;

import com.google.gson.Gson;

import ovh.angrysoft.homedaemon.connections.TcpConnection;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

class YeelightNotification {
    private String method;
    private HashMap<String, Object> params;

    public String getMethod() {
        return method;
    }

    public HashMap<String, Object> getParams() {
        return params;
    }

    public String toString() {
        return String.format("%s - %s", method, params);
    }
}

// TODO Delete this;
// class ParamsValues {
// private String power;
// private int bright;
// private int ct;
// private int rgb;
// private int hue;
// private int sat;
// private int color_mode;
// private int flowing;
// private int delayoff;

// public String toString() {
// return String.format("Power: %s\n bright: %s", power, bright);
// }

// public String getPower() {
// return power == null ? "" : power;
// }

// public int getBright() {
// return bright;
// }

// public int getCt() {
// return ct;
// }

// public int getRgb() {
// return rgb;
// }

// public int getHue() {
// return hue;
// }

// public int getSat() {
// return sat;
// }

// public int getColor_mode() {
// return color_mode;
// }

// public int getDelayoff() {
// return delayoff;
// }

// public int getFlowing() {
// return flowing;
// }

// }

public class YeelightWatcher extends Watcher {
    private String ip;
    private int port;

    public YeelightWatcher(String sid, String ip, int port) {
        super(sid);
        this.ip = ip;
        this.port = port;
    }

    @Override
    public void run() {
        try (TcpConnection conn = new TcpConnection(ip, port)) {
            while (true) {
                String rec = conn.recv();
                System.out.println(rec);
                YeelightNotification notify = new Gson().fromJson(rec, YeelightNotification.class);
                HashMap<String, Object> params = notify.getParams();
                params.forEach((k, v) -> {
                    Object value;
                    switch (k) {
                        case "power":
                            value = (String) v;
                            break;
                        case "bright":
                        case "ct":
                        case "rgb":
                        case "hue":
                        case "sat":
                        case "color_mode":
                        case "flowing":
                        case "delayoff":
                            Double tmp = (double) v;
                            value = tmp.intValue();
                            break;
                        default:
                            value = v;
                    }
                    handler.call(new StatusMessage(sid, k, value));
                });
            }
        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }

}
