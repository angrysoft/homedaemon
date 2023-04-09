package ovh.angrysoft.homedaemon.automation.conditions;

public class IntEqTestCase extends TestCase<Integer> {

    public IntEqTestCase(String type, String deviceSid, String attrName, Integer attrValue) {
        super(type, deviceSid, attrName, attrValue);
    }

    @Override
    public boolean check(Object value) {
        if (value == null)
            return false;
        return attrValue.equals(value);
    }

}
