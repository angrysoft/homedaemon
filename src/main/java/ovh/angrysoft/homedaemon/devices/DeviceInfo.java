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

    private Map<String, String> args;
    
    public Map<String, String> getArgs() {
        return args;
    }
    
}
