package ovh.angrysoft.homedaemon.config;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

public class ConfigTest {
    @Test
    @DisplayName("Test config set category/value")
    void testSet() {
        Config conf = new Config();
        JsonObject cat = new JsonObject();
        cat.add("enable", new JsonPrimitive(true));
        conf.setCategory("debug", cat);
        boolean enable = conf.get("debug", "enable").getAsBoolean();
        assertTrue(enable);
    }

    @Test
    @DisplayName("Test Load from dir")
    void testLoadFromFile() throws IOException {
        Config config = new Config();
        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        config.loadConfigs("src/test/java/ovh/angrysoft/homedaemon/config");
        assertEquals("stringTwo", config.get("test", "two").getAsString());
        assertEquals(1, config.get("test", "one").getAsInt());
        assertEquals(config.categorySet().size(), 2);
    }

}
