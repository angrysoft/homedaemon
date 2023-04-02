package ovh.angrysoft.homedaemon.automation;

public class Case {
    private String type;
    private String deviceSid;
    private String attrName;
    private Object attrValue;

    public Case(String type, String deviceSid, String attrName, Object attrValue) {
        this.type = type;
        this.deviceSid = deviceSid;
        this.attrName = attrName;
        this.attrValue = attrValue;
    }

    public boolean check() {
        return false;
    }

}
