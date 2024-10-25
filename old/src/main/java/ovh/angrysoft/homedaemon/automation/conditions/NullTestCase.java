package ovh.angrysoft.homedaemon.automation.conditions;

public class NullTestCase extends TestCase<Object> {

    public NullTestCase(String type, String deviceSid, String attrName, Object attrValue) {
        super(type, deviceSid, attrName, attrValue);
    }

    @Override
    public boolean check(Object value) {
        return true;
    }

}
