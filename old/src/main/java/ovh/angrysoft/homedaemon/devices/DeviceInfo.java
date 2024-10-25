package ovh.angrysoft.homedaemon.devices;

import java.util.Map;
import java.util.Objects;

public class DeviceInfo {
    private String sid;
    private String type;
    private String manufacturer;
    private String model;
    private String driver;
    private Map<String, String> name;
    private Map<String, String> place;
    private Map<String, String> args;
    
    public DeviceInfo(String sid, String type, String manufacturer, String model, Map<String, String> name,
            Map<String, String> place, String driver, Map<String, String> args) {
        this.sid = sid;
        this.type = type;
        this.manufacturer = manufacturer;
        this.model = model;
        this.name = name;
        this.place = place;
        this.driver = driver;
        this.args = args;
    }


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

    public String getDriver() {
        return driver;
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
        if (sid == null || sid.isEmpty())
            throw new VerifyError("sid is null");

        if (type == null)
            throw new VerifyError("type is null");

        if (manufacturer == null)
            throw new VerifyError("manufacturer is null");

        if (model == null)
            throw new VerifyError("model is null");

        if (name == null)
            throw new VerifyError("name is null");
        
        if  (driver == null || driver.isEmpty())
            throw new VerifyError("driver is null");

        if (place == null)
            throw new VerifyError("place is null");

        if (args == null)
            throw new VerifyError("args is null");
    }

    @Override
    public boolean equals(Object arg0) {
        if (!(arg0 instanceof DeviceInfo))
            return false;
        DeviceInfo deviceInfo = (DeviceInfo) arg0;
        if (this.sid == deviceInfo.getSid())
            return true;
        return false;
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.sid);
    }

}
