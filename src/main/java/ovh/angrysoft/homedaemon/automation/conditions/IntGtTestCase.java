package ovh.angrysoft.homedaemon.automation.conditions;

public class IntGtTestCase extends TestCase<Long> {

    public IntGtTestCase(String type, String deviceSid, String attrName, Object attrValue) {
        super(type, deviceSid, attrName, (Long) attrValue);
    }

    @Override
    public boolean check(Object value) {
        if (value == null)
            return false;
        return  (Long) value > attrValue;
    }

}
