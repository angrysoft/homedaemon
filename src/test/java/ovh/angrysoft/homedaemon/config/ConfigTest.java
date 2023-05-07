package ovh.angrysoft.homedaemon.config;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

public class ConfigTest {

    @Test
    void testRegisterAndLoadConfig() {
        Config config = new Config("src/test/java/ovh/angrysoft/homedaemon/config");

        config.resisterConfigType("test", new ConfigType<TestConfig>(TestConfig.class));
    }

    @Test
    void testGet() {
        Config config = new Config("src/test/java/ovh/angrysoft/homedaemon/config");
        config.resisterConfigType("test", new ConfigType<TestConfig>(TestConfig.class));
        TestConfig conf = (TestConfig) config.get("test");
        System.out.println(conf.one());
        assertEquals(1, conf.one());
        assertEquals("stringTwo", conf.two());
        assertEquals(1.1, conf.three());
    }
}

record TestConfig(Integer one, String two, Double three) {
}