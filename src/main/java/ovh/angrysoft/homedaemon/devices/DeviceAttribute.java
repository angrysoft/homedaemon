package ovh.angrysoft.homedaemon.devices;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class DeviceAttribute<T> {
    private T value;
    private final String name;
    private boolean readonly = false;
    private boolean initValue = true;
    private AttributeUpdateBehavior behavior;

    public DeviceAttribute(String name, T value) {
        this(name, value, false, AttributeUpdateBehavior.NORMAL);
    }

    public DeviceAttribute(String name, T value, boolean readonly) {
        this(name, value, readonly, AttributeUpdateBehavior.NORMAL);
    }

    public DeviceAttribute(String name, T value, boolean readonly, AttributeUpdateBehavior behavior) {
        this.name = name;
        this.readonly = readonly;
        this.value = value;
        this.behavior = behavior;
    }

    public AttributeUpdateBehavior getBehavior() {
        return behavior;
    }

    public void setBehavior(AttributeUpdateBehavior behavior) {
        this.behavior = behavior;
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

        if (!this.value.equals(value)) {
            this.value = value;
            ret = true;
        }

        switch(behavior) {
            case ALWAYS:
                ret = true;
                break;
            case IGNORE:
                ret = false;
                break;
            case NORMAL:
                break;
        }
        return ret;
    }

    public T getValue() {
        return this.value;
    }

}
