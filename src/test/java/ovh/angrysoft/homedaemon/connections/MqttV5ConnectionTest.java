package ovh.angrysoft.homedaemon.connections;

import java.util.HashMap;

import org.eclipse.paho.mqttv5.common.MqttException;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

public class MqttV5ConnectionTest {
    @Test
    @Tag("IntegrationTest")
    public void testSubscribe() {
        HashMap<String, Object> config = new HashMap<>();
        config.put("uri", "tcp://test.mosquito.org:1883");
        config.put("user", "wildcard");
        MqttV5Connection conn = new MqttV5Connection(config);
        conn.addTopic("#");
        conn.connect();
        int timeout = 0;
        while(timeout < 200) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            timeout++;
        }
    }

    @Test
    @Tag("IntegrationTest")
    public void testPublish() {
        HashMap<String, Object> config = new HashMap<>();
        // config.put("uri", "tcp://test.mosquito.org:1883");
        config.put("uri", "tcp://192.168.10.4:1883");
        config.put("user", "homedaemon");
        config.put("password", "spyb0tk34s");
        // config.put("timeout", 10000);
        // config.put("user", "wildcard");
        MqttV5Connection conn = new MqttV5Connection(config);
        conn.addTopic("homed/test");
        conn.connect();
        try {
            conn.publishMessage("test test test".getBytes(), 0, false, "homed/test");
        } catch (MqttException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        Integer timeout = 0;
        while(timeout < 20) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            timeout++;
            String msg = "Count to 20 : " + timeout.toString();
            try {
                conn.publishMessage(msg.getBytes(), 0, false, "homed/test");
            } catch (MqttException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

}
