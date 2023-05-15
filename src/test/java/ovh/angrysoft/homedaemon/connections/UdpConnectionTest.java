package ovh.angrysoft.homedaemon.connections;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

class UdpConnectionTest {
    private static EchoUdpTestServer srv;

    @BeforeAll
    public static void setup() throws DeviceConnectionError, SocketException {
        srv = new EchoUdpTestServer();
        srv.start();
    }

    @Test
    @DisplayName("Udp Send")
    void sendAndGetEcho() throws DeviceConnectionError {
        try (UdpConnection client = new UdpConnection()) {
            client.send("hello from client", "localhost", 6666);
            String echo = client.recv();
            System.out.println(echo.length());
            assertEquals("hello from server", echo);

        }
    }

    /*
     * @Test
     * void sendJsonAndGetEcho() {}
     */

    @AfterAll
    static void tearDown() throws DeviceConnectionError {
        srv.end();
    }
}

class EchoUdpTestServer extends Thread {

    private boolean running;

    public EchoUdpTestServer() throws SocketException {

    }

    public void run() {
        running = true;

        while (running) {
            try (DatagramSocket socket = new DatagramSocket(6666)) {
                byte[] bufIn = new byte[1024];
                DatagramPacket packet = new DatagramPacket(bufIn, bufIn.length);
                socket.receive(packet);

                InetAddress address = packet.getAddress();
                int port = packet.getPort();
                byte[] bufOut = "hello from server\n".getBytes();

                DatagramPacket ret = new DatagramPacket(bufOut, bufOut.length, address, port);
                socket.send(ret);
            } catch (IOException e) {
                System.err.println(e);
                running = false;
                continue;
            }
        }
    }

    public void end() {
        running = false;
    }
}