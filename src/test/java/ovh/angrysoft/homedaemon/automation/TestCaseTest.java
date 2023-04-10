package ovh.angrysoft.homedaemon.automation;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.automation.conditions.IntGtTestCase;
import ovh.angrysoft.homedaemon.automation.conditions.IntLtTestCase;
import ovh.angrysoft.homedaemon.automation.conditions.StatusTestCase;

public class TestCaseTest {
    @Test
    public void testIntGtTestCase() {
        assertTrue(new IntGtTestCase("status", "123", "state", 4).check(5));
        assertFalse(new IntGtTestCase("status", "123", "state", 4).check(1));
    }

    @Test
    public void testIntLtTestCase() {
        assertTrue(new IntLtTestCase("status", "123", "state", 4).check(1));
        assertFalse(new IntLtTestCase("status", "123", "state", 4).check(5));
    }

    @Test
    public void testIntEqTestCase() {
        assertTrue(new StatusTestCase("status", "123", "stateString", 11).check(11));
        assertFalse(new StatusTestCase("status", "123", "stateString", 11).check(1));
    }

    @Test
    public void testStatusTestCase() {
        assertTrue(new StatusTestCase("status", "123", "stateString", "foo").check("foo"));
        assertFalse(new StatusTestCase("status", "123", "stateString", "foo").check("bar"));
    }

}
