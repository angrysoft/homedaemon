package ovh.angrysoft.homedaemon.discover.yeelight;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.Objects;

import ovh.angrysoft.homedaemon.discover.DeviceDiscoverInfo;

public class YeelightDeviceInfo implements DeviceDiscoverInfo {
    private String sid;
    private String power;
    private String addr;
    private int port;
    private String model;
    private String[] support;
    private int bright;
    private int colorMode;
    private int ct;
    private int rgb;
    private int hue;
    private int sat;

    public YeelightDeviceInfo(String dev) {
        for (String line : dev.split("\r\n")) {
            if (!line.contains(":"))
                continue;
            String[] item = line.split(":", 2);
            String name = item[0].strip();
            String value = item[1].strip();
            switch (name) {
                case "id":
                    this.sid = value;
                    break;

                case "power":
                    this.power = value;
                    break;

                case "Location":
                    try {
                        URL url = new URL(value.replace("yeelight", "http"));
                        this.addr = url.getHost();
                        this.port = url.getPort();
                    } catch (MalformedURLException e) {
                        System.err.println(e);
                    }
                    break;

                case "model":
                    this.model = value;
                    break;

                case "support":
                    this.support = value.split(" ");
                    break;

                case "bright":
                    this.bright = Integer.parseInt(value);
                    break;

                case "color_mode":
                    this.colorMode = Integer.parseInt(value);
                    break;

                case "ct":
                    this.ct = Integer.parseInt(value);
                    break;

                case "rgb":
                    this.rgb = Integer.parseInt(value);
                    break;

                case "hue":
                    this.hue = Integer.parseInt(value);
                    break;

                case "sat":
                    this.sat = Integer.parseInt(value);
                    break;
            }
        }
    }

    public String getSid() {
        return this.sid;
    }

    public String getPower() {
        return this.power;
    }

    public String getAddr() {
        return this.addr;
    }

    public int getPort() {
        return this.port;
    }

    public String getModel() {
        return this.model;
    }

    public String[] support() {
        return this.support;
    }

    public int getBright() {
        return this.bright;
    }

    public int getColorMode() {
        return this.colorMode;
    }

    public int getCt() {
        return this.ct;
    }

    public int getRGB() {
        return this.rgb;
    }

    public int getHue() {
        return this.hue;
    }

    public int getSat() {
        return this.sat;
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.sid, this.model);
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof YeelightDeviceInfo))
            return false;
        YeelightDeviceInfo yi = (YeelightDeviceInfo) o;
        return this.sid.equals(yi.getSid()) && this.getModel().equals(yi.getModel());
    }

}
