package ovh.angrysoft.homedaemon.connections;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class HttpConnectionTest {
    static HttpConnection hConnection;

    @BeforeAll
    static void setup() {
        hConnection = new HttpConnection();
    }

    @Test
    void testGet() {
        hConnection.get("https://lide.pl/api/v1/offers");
    }

    @Test
    void testGet2() {
        hConnection.get("https://lide.pl/api/v1/posts");
    }
}
