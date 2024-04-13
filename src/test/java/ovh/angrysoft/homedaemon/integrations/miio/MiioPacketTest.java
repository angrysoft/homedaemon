package ovh.angrysoft.homedaemon.integrations.miio;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class MiioPacketTest {
    private final String TOKEN = "6764a7ec0f7b896736fb241f5c00c804";


    @Test
    void testDecrypt() {
        var m = new MiioPacket(TOKEN);
        String msg = "some message";
        var decrypted = m.decrypt(msg.getBytes());
        assertEquals(msg, new String(decrypted));
    }

}
