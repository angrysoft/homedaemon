package ovh.angrysoft.homedaemon.devices;

import java.util.Map;

public class DeviceInfo {
    private String sid;
    private String type;
    private String manufacturer;
    private String model;
    private String statusWatcher;
    private Map<String, String> name;
    private Map<String, String> place;
    private Map<String, String> args;

    public String getSid() {
        return sid;
    }

    public String getType() {
        return type;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public String getModel() {
        return model;
    }

    public String getStatusWatcher() {
        return statusWatcher;
    }

    public Map<String, String> getName() {
        return name;
    }

    public Map<String, String> getPlace() {
        return place;
    }

    public Map<String, String> getArgs() {
        return args;
    }

    public void checkFields() throws VerifyError {
        if (sid == null)
            throw new VerifyError("sid is null");

        if (type == null)
            throw new VerifyError("type is null");

        if (manufacturer == null)
            throw new VerifyError("manufacturer is null");

        if (model == null)
            throw new VerifyError("model is null");

        if (name == null)
            throw new VerifyError("name is null");

        if (place == null)
            throw new VerifyError("place is null");

        if (args == null)
            throw new VerifyError("args is null");
    }

}
