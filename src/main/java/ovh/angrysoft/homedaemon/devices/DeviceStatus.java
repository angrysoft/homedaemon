package ovh.angrysoft.homedaemon.devices;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class DeviceStatus {
    private final Map<String, DeviceAttribute<?>> attributes;

    public DeviceStatus() {
        this.attributes = new ConcurrentHashMap<>();
    }

    public <T> void registerAttribute(DeviceAttribute<T> attr) throws AttributeAlreadyExist {
        if (this.attributes.containsKey(attr.getName())) {
            throw new AttributeAlreadyExist(
                    String.format("Attribute %s already registered", attr.getName()));
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

    public Map<String, Object> getAll() {
        HashMap<String, Object> ret = new HashMap<>();
        for (Map.Entry<String, DeviceAttribute<?>> attr : attributes.entrySet()) {
            String key = attr.getKey();
            DeviceAttribute<?> value = attr.getValue();
            ret.put(key, value.getValue());
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
    // java 21
    // public boolean isValueEquals(String attrName, Object value) {
    // Object attr = attributes.get(attrName);
    // if (attr == null)
    // return false;

    // switch (value) {
    // case null -> {
    // return false;
    // }

    // default -> {

    // }
    // }
    // return true;
    // }
}
