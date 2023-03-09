package ovh.angrysoft.homedaemon.devices.yeelight;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Map;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

public class YeelightApiTest {
    @Test
    @DisplayName("Yeelight api set power test")
    public void setPowerTest() {
        try {
            YeelightApi api = new YeelightApi("192.168.10.27", 55443);
            api.setPower(true, PowerModes.NORMAL);
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            api.setPower(false, PowerModes.NORMAL);

        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }

    @Test
    @DisplayName("Yeelight api test set bright")
    public void setBrightTest() {
        try {
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

        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }

    @Test
    @DisplayName("Yeelight api test set ct")
    public void setCtTest() {
        try {
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

        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }

    @Test
    @DisplayName("Yeelight api get prop")
    public void getPropTest() {
        try {
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
        } catch (DeviceConnectionError e) {
            e.printStackTrace();
        }
    }
}
