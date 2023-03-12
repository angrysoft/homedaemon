package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class DeviceAttribute<T> {
    private T value;
    private String name;
    private boolean readonly = false;
    
    public DeviceAttribute(String name, T value) {
        this.name = name;
        this.value = value;
    }
    
    public DeviceAttribute(String name, T value, boolean readonly) {
        this.name = name;
        this.readonly = readonly;
        this.value = value;
    }
    

    
    public String getName() {
        return this.name;
    }
    
    public synchronized boolean setValue(T value) throws AttributeReadOnly {
        if (this.readonly && this.value != null) {
                throw new AttributeReadOnly("Read only parameter");
        }
        if (this.value != value) {
            this.value = value;
            return true;
        }
        return false;
    }
    
    public T getValue() {
        return this.value;
    }
}

