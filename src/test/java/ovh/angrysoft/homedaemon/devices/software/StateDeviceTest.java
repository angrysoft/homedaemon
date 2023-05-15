package ovh.angrysoft.homedaemon.devices.software;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.HashMap;
import java.util.Map;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;

public class StateDeviceTest {

    @Test
    @DisplayName("test send cmd")
    @Tag("IntegrationTest")
    public void status() throws AttributeReadOnly {
        Map<String, String> stateName = new HashMap<>();
        stateName.put("pl", "Stan");
        stateName.put("en", "State");
        Map<String, String> statePlace = new HashMap<>();
        statePlace.put("pl", "Wszędzie");
        statePlace.put("en", "everywhere");
        DeviceInfo stateInfo = new DeviceInfo(
                "state",
                "state",
                "homedaemon",
                "state",
                stateName,
                statePlace,
                "software.StateDevice",
                new HashMap<>());
        StateDevice stateDevice = new StateDevice(stateInfo);
        stateDevice.registerStateAttribute(new DeviceAttribute<Boolean>("attr1", false));
        assertEquals(false, stateDevice.query("attr1"));

        stateDevice.updateStatus("attr1", true);
        assertEquals(true, stateDevice.query("attr1"));
    }

}
