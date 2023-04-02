package ovh.angrysoft.homedaemon.automation.conditions;

public class IntLtTestCase extends TestCase<Long> {

    public IntLtTestCase(String type, String deviceSid, String attrName, Object attrValue) {
        super(type, deviceSid, attrName, (Long) attrValue);
    }

    @Override
    public boolean check(Object value) {
        if (value == null)
            return false;
        return  (Long) value < attrValue;
    }

}
