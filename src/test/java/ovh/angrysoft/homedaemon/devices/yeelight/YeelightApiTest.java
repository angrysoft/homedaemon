package ovh.angrysoft.homedaemon.devices.yeelight;

import static org.junit.jupiter.api.Assertions.assertEquals;
import java.util.Map;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class YeelightApiTest {
    @Test
    @DisplayName("Yeelight api set power test")
    @Tag("IntegrationTest")
    void setPowerTest() {
        YeelightApi api = new YeelightApi("192.168.10.27", 55443);
        api.setPower(true, PowerModes.NORMAL);
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        api.setPower(false, PowerModes.NORMAL);
    }

    @Test
    @DisplayName("Yeelight api test set bright")
    @Tag("IntegrationTest")
    void setBrightTest() {
        YeelightApi api = new YeelightApi("192.168.10.27", 55443);
        try {
            api.setDuration(2000);
            api.setPower(true, PowerModes.NORMAL);
            Thread.sleep(2000);
            api.setBright(100);
            Thread.sleep(2000);
            api.setBright(1);
            Thread.sleep(2000);
            api.setPower(false, PowerModes.NORMAL);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Test
    @DisplayName("Yeelight api test set ct")
    @Tag("IntegrationTest")
    void setCtTest() {
        YeelightApi api = new YeelightApi("192.168.10.27", 55443);
        try {
            api.setPower(true, PowerModes.NORMAL);
            Thread.sleep(2000);
            api.setCtAbx(6500);
            Thread.sleep(2000);
            api.setCtAbx(2700);
            Thread.sleep(2000);
            api.setPower(false, PowerModes.NORMAL);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Test
    @DisplayName("Yeelight api get prop")
    @Tag("IntegrationTest")
    void getPropTest() {
        YeelightApi api = new YeelightApi("192.168.10.27", 55443);
        String[] props = { "power", "ct", "bright" };
        Map<String, Object> ret = api.getProp(props);
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        if (ret == null) {
            return;
        }
        ret.forEach((k, v) -> System.out.println(k + " : " + v));
        assertEquals(3, ret.size());
    }
}
