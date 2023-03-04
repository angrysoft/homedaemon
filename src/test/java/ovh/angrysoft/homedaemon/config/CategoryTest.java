package ovh.angrysoft.homedaemon.config;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class CategoryTest {
    @Test
    @DisplayName("Set category value")
    void testSetValue() {
        Category cat = new Category();
        cat.set("dev-dir", "/etc/homedaemon/dev.d");
        assertEquals(cat.get("dev-dir"), "/etc/homedaemon/dev.d");
    }
}
