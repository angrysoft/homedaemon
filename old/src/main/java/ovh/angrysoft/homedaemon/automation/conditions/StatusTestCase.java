package ovh.angrysoft.homedaemon.automation.conditions;

public class StatusTestCase extends TestCase<Object> {

    public StatusTestCase(String type, String deviceSid, String attrName, Object attrValue) {
        super(type, deviceSid, attrName, attrValue);
    }

    @Override
    public boolean check(Object value) {
        if (value == null)
            return false;
        return attrValue.equals(value);
    }

}
