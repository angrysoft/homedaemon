package ovh.angrysoft.homedaemon.connections.ewelink;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class AuthTokenTest {
    @Test
    void testTokenGenerating() {
        String expected = "SIIVKeNgdwPmcBeagrLafZ8twmB2h4RTKUYNgw+TETg=";
        assertEquals(expected, AuthToken.getToken("testDataToken", "OdPuCZ4PkPPi0rVKRVcGmll2NM6vVk0c"));
    }
}
