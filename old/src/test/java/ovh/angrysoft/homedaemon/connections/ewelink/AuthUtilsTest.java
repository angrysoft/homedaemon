package ovh.angrysoft.homedaemon.connections.ewelink;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class AuthUtilsTest {
    @Test
    void testTokenGenerating() {
        String expected = "SIIVKeNgdwPmcBeagrLafZ8twmB2h4RTKUYNgw+TETg=";
        assertEquals(expected,
                AuthUtils.getAuthToken("testDataToken", "OdPuCZ4PkPPi0rVKRVcGmll2NM6vVk0c"));
    }

    @Test
    void testEncryptDecrypt() {
        final String key = "2dd66958-c072-4e58-a296-c3f7a2e91d3f";
        String data = "foo bar";
        String[] encrypted = AuthUtils.encryptData(data, key);
        String decrypted = AuthUtils.decryptData(encrypted[0], key, encrypted[1]);
        assertEquals(data, decrypted);
    }
}
