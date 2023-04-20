package ovh.angrysoft.homedaemon.discover.yeelight;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import ovh.angrysoft.homedaemon.discover.DeviceDiscoverInfo;

public class YeelightDeviceInfo implements DeviceDiscoverInfo {
    private Map<String, Object> info;

    public YeelightDeviceInfo(String dev) {
        info = new HashMap<>();

        for (String line : dev.split("\r\n")) {
            if (!line.contains(":"))
                continue;
            String[] item = line.split(":", 2);
            String name = item[0].strip();
            String value = item[1].strip();
            switch (name) {
                case "id":
                    info.put("id", value);
                    break;

                case "power":
                    info.put("power", value);
                    break;

                case "Location":
                    try {
                        URL url = new URL(value.replace("yeelight", "http"));
                        info.put("addr", url.getHost());
                        info.put("port", url.getPort());
                    } catch (MalformedURLException e) {
                        System.err.println(e);
                    }
                    break;

                case "model":
                    info.put("model", value);

                    break;

                case "support":
                    info.put("support", value.split(" "));
                    break;

                case "bright":
                    info.put("bright", Integer.parseInt(value));
                    break;

                case "color_mode":
                    info.put("colorMode", Integer.parseInt(value));
                    break;

                case "ct":
                    info.put("ct", Integer.parseInt(value));
                    break;

                case "rgb":
                    info.put("rgb", Integer.parseInt(value));
                    break;

                case "hue":
                    info.put("hue", Integer.parseInt(value));
                    break;

                case "sat":
                    info.put("sat", Integer.parseInt(value));
                    break;
            }
        }
    }

    // @SuppressWarnings("unchecked")
    public <T> T get(String key) {
        return (T) this.info.get(key);
    }

    public String getDeviceSid() {
        return (String) this.info.get("sid");
    }

    @Override
    public int hashCode() {
        return Objects.hash(info.get("sid"), info.get("model"));
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof YeelightDeviceInfo))
            return false;
        YeelightDeviceInfo yi = (YeelightDeviceInfo) o;
        return getDeviceSid().equals(yi.getDeviceSid()) && info.get("model").equals(yi.get("model"));
    }

    @Override
    public boolean containsKey(String key) {
        return info.containsKey(key);
    }

}
