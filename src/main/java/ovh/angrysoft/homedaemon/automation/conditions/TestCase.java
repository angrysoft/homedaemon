package ovh.angrysoft.homedaemon.automation.conditions;

public abstract class TestCase<T> {
    protected final String type;
    protected final String deviceSid;
    protected final String attrName;
    protected final T attrValue;

    public TestCase(String type, String deviceSid, String attrName, T attrValue) {
        this.type = type;
        this.deviceSid = deviceSid;
        this.attrName = attrName;
        this.attrValue = attrValue;
    }

    public abstract boolean check(Object value);

    public String getType() {
        return type;
    }

    public String getDeviceSid() {
        return deviceSid;
    }

    public String getAttrName() {
        return attrName;
    }

    public T getAttrValue() {
        return attrValue;
    }

}
