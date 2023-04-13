package ovh.angrysoft.homedaemon.automation.conditions;

public class IntGtTestCase extends TestCase<Integer> {

    public IntGtTestCase(String type, String deviceSid, String attrName, Integer attrValue) {
        super(type, deviceSid, attrName, attrValue);
    }

    @Override
    public boolean check(Object value) {
        if (value == null)
            return false;
        return (Integer) value > attrValue;
    }
}
