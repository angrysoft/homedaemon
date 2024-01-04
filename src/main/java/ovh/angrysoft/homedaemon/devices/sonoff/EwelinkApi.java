package ovh.angrysoft.homedaemon.devices.sonoff;

import java.util.HashMap;
import java.util.Map;
import com.google.gson.Gson;
import ovh.angrysoft.homedaemon.connections.HttpConnection;
import ovh.angrysoft.homedaemon.connections.ewelink.AuthUtils;


/*
 * on: the device is on when power supply is recovered. off: the device is off when power supply is
 * recovered. stay: the device status keeps as the same as the state before power supply is gone
 */
enum PowerState {
    ON, OFF, STAY
}


public class EwelinkApi {
    HttpConnection conn = new HttpConnection();
    int port;
    String ip;
    String sid;
    boolean encrypt;
    String deviceKey;

    public EwelinkApi(String ip, int port, String sid) {
        this.ip = ip;
        this.port = port;
        this.sid = sid;
        this.encrypt = false;
    }

    public EwelinkApi(String ip, int port, String sid, String deviceKey) {
        this.ip = ip;
        this.port = port;
        this.sid = sid;
        this.deviceKey = deviceKey;
    }

    public void setSwitch(boolean state) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("switch", state ? "on" : "off");
        send("zeroconf/switch", payload);
    }

    public void setSwitches(boolean state, int outlet) {
        Map<String, Object> switches = new HashMap<>();
        Map<String, Object> payload = new HashMap<>();

        payload.put("switch", state ? "on" : "off");
        payload.put("outlet", outlet);

        switches.put("switches", new Map[] {payload});
        send("zeroconf/switches", switches);
    }

    public void setBright(int brightness) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("switch", "on");
        payload.put("brightness", brightness);
        send("zeroconf/dimmable", payload);
    }

    public void setStartup(PowerState startup) {
        Map<String, Object> payload = new HashMap<>();
        String arg = "";
        switch (startup) {
            case PowerState.ON:
                arg = "on";
                break;

            case PowerState.OFF:
                arg = "off";
                break;

            case PowerState.STAY:
                arg = "stay";
                break;
            default:
                break;
        }
        payload.put("startup", arg);
        send("zeroconf/startup", payload);
    }

    public void setPulse(boolean pulseState, int pulseWidth) {
        // check range 500~3600000
        Map<String, Object> payload = new HashMap<>();
        payload.put("pulse", pulseState ? "on" : "off");
        payload.put("pulseWidth", pulseWidth);
        send("zeroconf/pulse", payload);
    }

    public void setPulses(boolean pulseState, int pulseWidth, int outlet) {
        // check range 500~3600000
        Map<String, Object> configure = new HashMap<>();
        Map<String, Object> payload = new HashMap<>();
        payload.put("pulse", pulseState ? "on" : "off");
        payload.put("pulseWidth", pulseWidth);
        payload.put("outlet", outlet);
        configure.put("configure", new Map[] {payload});
        send("zeroconf/pulses", configure);
    }

    public void setWifi(String ssid, String password) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("ssid", ssid);
        payload.put("password", password);
        send("zeroconf/wifi", payload);
    }

    public void otaUnlock() {
        Map<String, Object> payload = new HashMap<>();
        send("zeroconf/ota_unlock", payload);
        // TODO: error codes
    }

    public void otaFlash(String url, String sha256Sum) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("downloadUrl", url);
        payload.put("sha256sum", sha256Sum);
        send("zeroconf/ota_flash", payload);
        // TODO: error codes

    }

    public EwelinkDeviceInfoResponse getInfo() {
        Map<String, Object> payload = new HashMap<>();
        Gson json = new Gson();
        String response = send("zeroconf/ota_unlock", payload);
        return json.fromJson(response, EwelinkDeviceInfoResponse.class);
    }

    String send(String path, Object payload) {
        Gson json = new Gson();
        Map<String, Object> toSend = new HashMap<>();
        toSend.put("deviceid", sid);
        if (encrypt) {
            String[] encrypted = AuthUtils.encryptData(json.toJson(payload), deviceKey);
            toSend.put("data", encrypted[0]);
            toSend.put("iv", encrypted[1]);
            toSend.put("encrypt", true);
        } else {
            toSend.put("data", payload);
        }
        String uriString = new StringBuilder().append("http://").append(ip).append(":").append(port)
                .append("/").append(path).toString();
        
        return conn.post(uriString, json.toJson(toSend));
    }
}
