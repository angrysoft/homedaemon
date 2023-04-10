package ovh.angrysoft.homedaemon.devices.yeelight;

import java.util.HashMap;
import java.util.Map;

import com.google.gson.Gson;

import ovh.angrysoft.homedaemon.connections.IdGen;
import ovh.angrysoft.homedaemon.connections.TcpConnection;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

class Command {
    private int id;
    private String method;
    private Object[] params;

    public Command(int id, String method, Object[] params) {
        this.id = id;
        this.method = method;
        this.params = params;
    }

    public int getId() {
        return id;
    }

    public String getMethod() {
        return method;
    }

    public Object[] getParams() {
        return params;
    }
}

class CommandResult {
    private int id;
    private Object[] result;
    private ResultError error;

    public int getId() {
        return id;
    }

    public Object[] getResult() {
        return result;
    }

    public ResultError getError() {
        return error;
    }
}

enum PowerModes {
    NORMAL,
    CT,
    RGB,
    HSV,
    COLOR,
    NIGHT
}

class ResultError {
    private int code;
    private String message;

    public int getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }
}

class YeelightApi {
    private IdGen commandId;
    private String ip;
    private int port;
    private String efx;
    private int duration;
    private int minCt;
    private int maxCt;

    public YeelightApi(String ip, int port) throws DeviceConnectionError {
        this.commandId = new IdGen();
        this.ip = ip;
        this.port = port;
        this.efx = "smooth";
        this.duration = 500;
        this.minCt = 1700;
        this.maxCt = 6500;
    }

    public void setEfx(String efx) {
        this.efx = efx;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public String getEfx() {
        return efx;
    }

    public int getDuration() {
        return duration;
    }

    public void setMinCt(int minCt) {
        this.minCt = minCt;
    }

    public int getMinCt() {
        return minCt;
    }

    public void setMaxCt(int maxCt) {
        this.maxCt = maxCt;
    }

    public int getMaxCt() {
        return maxCt;
    }

    /**
     * This method is used to retrieve current property of smart LED.
     * 
     * @param props (str): Variable length argument name of property to retrieve
     *              (max 18 in
     *              one)
     *              <ul>
     *              <li>power on - smart LED is turned on / off: smart LED is turned
     *              off</li>
     *              <li>bright - Brightness percentage. Range 1 ~ 100</li>
     *              <li>ct - Color temperature. Range 1700 ~ 6500(k)</li>
     *              <li>rgb - Color. Range 1 ~ 16777215</li>
     *              <li>hue - Hue. Range 0 ~ 359</li>
     *              <li>sat - Saturation. Range 0 ~ 100</li>
     *              <li>color_mode - 1: rgb mode / 2: color temperature mode / 3:
     *              hsv mode</li>
     *              <li>flowing - 0: no flow is running / 1:color flow is
     *              running</li>
     *              <li>delayoff - The remaining time of a sleep timer. Range 1 ~
     *              60</li>
     *              <li>(minutes)</li>
     *              <li>flow_params - Current flow parameters (only meaningful when
     *              'flowing'</li>
     *              <li>is 1)</li>
     *              <li>music_on - 1: Music mode is on / 0: Music mode is off</li>
     *              <li>name - The name of the device set by “set_name” command</li>
     *              <li>bg_power - Background light power status</li>
     *              <li>bg_flowing - Background light is flowing</li>
     *              <li>bg_flow_params - Current flow parameters of background
     *              light</li>
     *              <li>bg_ct - Color temperature of background light</li>
     *              <li>bg_mode - 1: rgb mode / 2: color temperature mode / 3: hsv
     *              mode</li>
     *              <li>bg_bright - Brightness percentage of background light</li>
     *              <li>bg_rgb - Color of background light</li>
     *              <li>bg_hue - Hue of background light</li>
     *              <li>bg_sat - Saturation of background light</li>
     *              <li>nl_br - Brightness of night mode light</li>
     *              <li>active_mode - ...</li>
     *              </ul>
     * @return Map of prop name and a value
     */
    public Map<String, Object> getProp(String[] props) {
        HashMap<String, Object> result = new HashMap<>();
        CommandResult answer = send("get_prop", props);
        if (props.length == answer.getResult().length) {
            for (int i = 0; i < props.length; i++) {
                result.put(props[i], answer.getResult()[i]);
            }
        }
        return result;
    }

    /**
     * This method is used to switch on or off the smart LED (software managed
     * on/off).
     * 
     * @param state (str): can only be `on` or `off`.
     *              `on` means turn on the smart LED, `off` means turn off the smart
     *              LED.
     * @param mode  mode
     *              <ul>
     *              <li>0: Normal turn on operation (default value)</li>
     *              <li>1: Turn on and switch to CT mode.</li>
     *              <li>2: Turn on and switch to RGB mode.</li>
     *              <li>3: Turn on and switch to HSV mode.</li>
     *              <li>4: Turn on and switch to color flow mode.</li>
     *              <li>5: Turn on and switch to Night light mode. (Ceiling light
     *              only).</li>
     *              </ul>
     */
    public void setPower(boolean state, PowerModes mode) {
        String powerState = state ? "on" : "off";
        Object[] params = { powerState, efx, duration, mode };
        send("set_power", params);
    }

    public void setPower(boolean state) {
        setPower(state, PowerModes.NORMAL);
    }

    public void toggle() {
        send("toggle", null);
    }

    /**
     * This method is used to change the color temperature of a smart LED.
     * 
     * @param ct The target color temperature.
     *           The type is integer and range is 1700 ~ 6500 (k).
     */
    public void setCtAbx(int ct) {
        Object[] params = { ct, efx, duration };
        send("set_ct_abx", params);
    }

    /**
     * This method is used to change the color temperature of a smart LED with
     * percent scale.
     * 
     * @param pc Percentage target color temperature.
     *           The type is integer and range is 0 ~ 100 (%).
     */
    public void setCtPc(int pc) {
        int colorTemp = minCt + ((maxCt - minCt) * pc / 100);
        setCtAbx(colorTemp);
    }

    /**
     * 
     * @param rgb
     */
    public void setColor(int rgb) {
        Object[] params = { rgb, efx, duration };
        send("set_rgb", params);
    }

    public void setRGB(int red, int green, int blue) {
        int rgb = (red << 16) + (green << 8) + blue;
        setColor(rgb);
    }

    public void setDefault() {
        send("set_default", null);
    }

    public void setBright(int bright) {
        Object[] params = { bright, efx, duration };
        send("set_bright", params);
    }

    private CommandResult send(String method, Object[] params) {
        int id = commandId.getId();
        CommandResult result = null;
        try (TcpConnection conn = new TcpConnection(ip, port)) {
            Command cmd = new Command(id, method, params);
            conn.send(new Gson().toJson(cmd));
            conn.send("\r\n");
            String answer = conn.recv();
            System.out.println(answer);
            result = new Gson().fromJson(answer, CommandResult.class);
        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
        return result;
    }
}
