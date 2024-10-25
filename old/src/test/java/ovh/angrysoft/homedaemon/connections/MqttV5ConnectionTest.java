package ovh.angrysoft.homedaemon.connections;

import org.eclipse.paho.mqttv5.common.MqttException;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

public class MqttV5ConnectionTest {
    @Test
    @Tag("IntegrationTest")
    public void testSubscribe() {
        MqttV5Connection conn = MqttV5Connection.builder()
                .uri("tcp://test.mosquito.org:1883")
                .timeout(5000)
                .build();
        conn.addTopic("#");
        conn.start();
        int timeout = 0;
        while (timeout < 200) {
            try {
                System.out.println("Tick");
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            timeout++;
        }
    }

    @Test
    @Tag("IntegrationTest")
    public void testConnectWithAuth() {
        MqttV5Connection conn = MqttV5Connection.builder()
                .uri("tcp://test.mosquito.org:1884")
                .user("ro")
                .password("readonly")
                .build();
        conn.addTopic("#");
        conn.start();

        int timeout = 0;
        while (timeout < 200) {
            try {
                System.out.println("Tick");
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            timeout++;
        }
    }

    @Test
    @Tag("IntegrationTest")
    public void testPublish() {
        MqttV5Connection conn = MqttV5Connection.builder()
                .uri("tcp://test.mosquito.org:1884")
                .user("rw")
                .password("readwrite")
                .build();
        conn.addTopic("#");
        conn.run();
        try {
            conn.publishMessage("test test test".getBytes(), 0, false, "homed/test");
        } catch (MqttException e) {
            e.printStackTrace();
        }
        Integer timeout = 0;
        while (timeout < 20) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            timeout++;
            String msg = "Count to 20 : " + timeout.toString();
            try {
                conn.publishMessage(msg.getBytes(), 0, false, "homed/test");
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

}
