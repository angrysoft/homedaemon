package ovh.angrysoft.homedaemon.watcher;

import com.google.gson.Gson;

import ovh.angrysoft.homedaemon.connections.TcpConnection;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

class YeelightNotification {
    private String method;
    private ParamsValues params;

    public String getMethod() {
        return method;
    }

    public ParamsValues getParams() {
        return params;
    }

    public String toString() {
        return String.format("%s - %s", method, params);
    }
}

class ParamsValues {
    private String power;
    private int bright;
    private int ct;
    private int rgb;
    private int hue;
    private int sat;
    private int color_mode;
    private int flowing;
    private int delayoff;

    public String toString() {
        return String.format("Power: %s\n bright: %s", power, bright);
    }

    public String getPower() {
        return power == null ? "" : power;
    }

    public int getBright() {
        return bright;
    }

    public int getCt() {
        return ct;
    }

    public int getRgb() {
        return rgb;
    }

    public int getHue() {
        return hue;
    }

    public int getSat() {
        return sat;
    }

    public int getColor_mode() {
        return color_mode;
    }

    public int getDelayoff() {
        return delayoff;
    }

    public int getFlowing() {
        return flowing;
    }

}

public class YeelightWatcher extends Watcher {
    private String ip;
    private int port;

    public YeelightWatcher(String ip, int port) {
        this.ip = ip;
        this.port = port;
    }

    @Override
    public void run() {
        try (TcpConnection conn = new TcpConnection(ip, port)) {
            while (true) {
                YeelightNotification notify = new Gson().fromJson(conn.recv(), YeelightNotification.class);
                System.err.println(notify.getParams().getCt());
            }
        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }

}
