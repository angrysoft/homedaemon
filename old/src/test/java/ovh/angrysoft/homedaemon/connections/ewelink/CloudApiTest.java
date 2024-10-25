package ovh.angrysoft.homedaemon.connections.ewelink;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class CloudApiTest {
    static CloudApi api;

    @BeforeAll
    static void setup() {
        api = new CloudApi.Builder().email("sebastian.zwierzchowski@gmail.com")
                .password("Spyb0tk34s").countryCode("+48").appId("4s1FXKC9FaGfoqXhmXSJneb3qcm1gOak")
                .appSecret("oKvCM06gvwkRbfetd6qWRrbC3rFrbIpV").build();
        Boolean result = api.login();
        System.err.println(result);
    }

    @Test
    @Tag("Online")
    void testGetDevices() {
        var devices = api.getDevices();
        System.out.println(devices.total());
        for (var thing: devices.thingList()) {
            System.out.println(thing.itemType());
            System.out.println(thing.itemData().name());
            System.out.println(thing.itemData().deviceid());
            System.out.println(thing.itemData().devicekey());
            System.out.println(thing.itemData().productModel());
        }
    }
}
