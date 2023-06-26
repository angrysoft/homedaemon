package ovh.angrysoft.homedaemon.automation.conditions;

public class IntLtTestCase extends TestCase<Integer> {

    public IntLtTestCase(String type, String deviceSid, String attrName, int attrValue) {
        super(type, deviceSid, attrName, attrValue);
    }

    @Override
    public boolean check(Object value) {
        if (value == null)
            return false;
        return  (int) value < attrValue;
    }

}
