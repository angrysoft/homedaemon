package ovh.angrysoft.homedaemon.automation.conditions;

public abstract class TestCase<E> {
    protected final String type;
    protected final String deviceSid;
    protected final String attrName;
    protected final E attrValue;

    public TestCase(String type, String deviceSid, String attrName, E attrValue) {
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

    public E getAttrValue() {
        return attrValue;
    }

}
