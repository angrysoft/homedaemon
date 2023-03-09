package ovh.angrysoft.homedaemon;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.util.HashMap;
import java.util.Map;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeNotFound;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceStatus;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;



public class DeviceStatusTest {
    DeviceStatus status;

    @BeforeEach
    void setUp() {
        status = new DeviceStatus();
    }

    @Test
    @DisplayName("Test Register attribute")
    void testRegisterAttribute() {
        try {
            status.registerAttribute( new DeviceAttribute<>("test", "StringValue") );
        } catch ( AttributeAlreadyExist e) {}
        assertEquals("StringValue", status.get("test"));
    }

    @Test
    @DisplayName("Unregister attribute")
    void testUnregisterAttribute() {
        try {
            status.registerAttribute( new DeviceAttribute<>("attrToRemove", "StringValue") );
        } catch ( AttributeAlreadyExist e) {}
        status.unregisterAttribute("attrToRemove");
        assertNull(status.get("attrToRemove"));
    }

    @Test
    @DisplayName("Add Attribute Alias")
    void testAddAlias() {
        try {
            status.registerAttribute( new DeviceAttribute<>("test", "StringValue") );
            status.addAlias("aliasName", "test");
        } catch ( AttributeAlreadyExist|AttributeNotFound e) {}

        assertEquals("StringValue", status.get("aliasName"));
    }

    @Test
    @DisplayName("Set Attribute")
    void testSetAttribute() {
        try {
            status.registerAttribute( new DeviceAttribute<>("test", "StringValue") );
            status.set("test", "newStringValue");
        } catch ( AttributeAlreadyExist| AttributeReadOnly e) {
        }

        assertEquals("newStringValue", status.get("test"));
    }

    @Test
    @DisplayName("Update Attributes")
    void testUpdateAttributes() {
        try {
            status.registerAttribute( new DeviceAttribute<>("attr1", "StringValue") );
            status.registerAttribute( new DeviceAttribute<>("attr2", 1) );
        } catch ( AttributeAlreadyExist e) {}

        HashMap<String, Object> toUpdate = new HashMap<>();
        toUpdate.put("attr1", "value1");
        toUpdate.put("attr2", 10);
        try {
            status.update(toUpdate);
        } catch ( AttributeReadOnly e) {

        }
        assertEquals("value1", status.get("attr1"));
        assertEquals(10, (int) status.get("attr2"));

    }

    @Test
    @DisplayName("Get all Attributes")
    void testGetAll() {
        try {
            status.registerAttribute( new DeviceAttribute<>("attr1", "value1") );
            status.registerAttribute( new DeviceAttribute<>("attr2", 1) );
        } catch ( AttributeAlreadyExist e) {}

        Map<String, String> stringAttrs = status.getAll();
        
        assertEquals("value1", stringAttrs.get("attr1"));
        assertEquals("1", stringAttrs.get("attr2"));

    }
    
}
