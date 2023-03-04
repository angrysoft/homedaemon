package ovh.angrysoft.homedaemon.config;

import java.io.IOException;
import java.util.HashMap;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class ConfigTest {
    @Test
    @DisplayName("Test config set category/value")
    void testSet() {
        Config conf = new Config();
        HashMap<String, Object> cat = new HashMap<>();
        cat.put("enable", true);
        conf.set("debug", cat);
    }

    @Test
    @DisplayName("Test Load from dir")
    void testLoadFromFile() throws IOException {
        Config config = new Config();
        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        config.loadFromDir("src/test/java/ovh/angrysoft/homedaemon/config");
        System.out.println(config.get("testlist", "io"));
        config.listCategory();
    }
}
