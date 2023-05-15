package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class DeviceAttribute<T> {
    private T value;
    private final String name;
    private boolean readonly = false;
    private boolean alwaysUpdate = false;
    private boolean initValue = true;

    public DeviceAttribute(String name, T value) {
        this(name, value, false, false);
    }

    public DeviceAttribute(String name, T value, boolean readonly) {
        this(name, value, readonly, false);
    }

    public DeviceAttribute(String name, T value, boolean readonly, boolean alwaysUpdate) {
        this.name = name;
        this.readonly = readonly;
        this.value = value;
        this.alwaysUpdate = alwaysUpdate;
    }

    public boolean isAlwaysUpdate() {
        return alwaysUpdate;
    }

    public void setAlwaysUpdate(boolean alwaysUpdate) {
        this.alwaysUpdate = alwaysUpdate;
    }

    public String getName() {
        return this.name;
    }

    public synchronized boolean setValue(T value) throws AttributeReadOnly {
        if (this.readonly) {
            throw new AttributeReadOnly("Read only parameter");
        }
        boolean ret = false;
        if (this.initValue) {
            this.initValue = false;
            ret = true;
        }

        if (this.alwaysUpdate || !this.value.equals(value)) {
            this.value = value;
            ret = true;
        }
        return ret;
    }

    public T getValue() {
        return this.value;
    }

}
