package ovh.angrysoft.homedaemon.devices;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;

public abstract class BaseDevice {
    protected DeviceStatus status;
    protected static final Logger LOGGER = Logger.getLogger("Homedaemon");

    protected BaseDevice(DeviceInfo deviceInfo) {
        this.status = new DeviceStatus();
        try {
            this.status.registerAttribute(new DeviceAttribute<>("sid", deviceInfo.getSid(),  true));
            this.status.registerAttribute(new DeviceAttribute<>("name", deviceInfo.getName()));
            this.status.registerAttribute(new DeviceAttribute<>("place", deviceInfo.getPlace()));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }

    }

    protected String getSid() {
        return this.status.get("sid");
    }

    public List<String> getTraits() {
        List<String> ret = new ArrayList<>();
        for (Class<?> cls : this.getClass().getInterfaces()) {
            String className = cls.getName();
            int lastDot = className.lastIndexOf(".");
            ret.add(className.substring(++lastDot));
        }
        return ret;
    }

    public <T> T query(String attrName) {
        return this.status.get(attrName);
    }

    public Map<String, String> getDeviceStatus() {
        HashMap<String, String> ret = new HashMap<>();
        ret.putAll(this.status.getAll());
        ret.put("traits", this.getTraits().toString());
        return ret;

    }

    public void execute(String methodName, Object arg) {
        
    }
}
