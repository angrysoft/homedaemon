package ovh.angrysoft.homedaemon.devices;

import java.util.HashMap;
import java.util.Map;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class DeviceStatus {
    private final HashMap<String, DeviceAttribute<?>> attributes;

    public DeviceStatus() {
        this.attributes = new HashMap<>();
    }

    public <T> void registerAttribute(DeviceAttribute<?> attr) throws AttributeAlreadyExist {
        if (this.attributes.containsKey(attr.getName())) {
            throw new AttributeAlreadyExist(String.format("Attribute %s already registered", attr.getName()));
        }
        this.attributes.put(attr.getName(), attr);
    }

    public void unregisterAttribute(String attrName) {
        if (this.attributes.containsKey(attrName)) {
            this.attributes.remove(attrName);
        }
    }

    public void addAlias(String aliasName, String attrName) throws AttributeNotFound {
        if (this.attributes.containsKey(attrName)) {
            this.attributes.put(aliasName, this.attributes.get(attrName));
        } else {
            throw new AttributeNotFound(String.format("Attribute %s not found", attrName));
        }
    }

    @SuppressWarnings("unchecked")
    public <T> T get(String attrName) {
        if (this.attributes.containsKey(attrName))
            return (T) this.attributes.get(attrName).getValue();
        return null;
    }

    public DeviceAttribute<?> getAttr(String attrName) {
        if (this.attributes.containsKey(attrName))
            return this.attributes.get(attrName);
        return null;
    }

    public Map<String, String> getAll() {
        HashMap<String, String> ret = new HashMap<>();
        for (Map.Entry<String, DeviceAttribute<?>> attr : attributes.entrySet()) {
            String key = attr.getKey();
            DeviceAttribute<?> value = attr.getValue();
            ret.put(key, value.getValue().toString());
        }
        return ret;
    }

    @SuppressWarnings("unchecked")
    public <T> boolean update(String attrName, T attrValue) throws AttributeReadOnly {
        try {
            
            if (this.attributes.containsKey(attrName)) {
                DeviceAttribute<T> attr = (DeviceAttribute<T>) this.attributes.get(attrName);
                return attr.setValue(attrValue);
            }

        } catch (ClassCastException e) {
            
        }
        return false;
    }

}
