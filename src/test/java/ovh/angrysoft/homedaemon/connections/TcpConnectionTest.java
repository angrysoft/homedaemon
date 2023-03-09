package ovh.angrysoft.homedaemon.connections;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

public class TcpConnectionTest {
    private static EchoTcpServer srv;

    @BeforeAll
    static void setup() throws DeviceConnectionError {
        srv = new EchoTcpServer(6666);
        srv.start();
    }

    @Test
    @DisplayName("TCP send")
    void sendAndGetEcho() throws DeviceConnectionError {
        try (TcpConnection client = new TcpConnection("localhost", 6666)) {
            client.send("hello tcp server\n");
            String echo = client.recv();
            System.out.println(echo);
            assertEquals("hello tcp client", echo);
        }
    }

    @AfterAll
    static void stop() throws DeviceConnectionError {
        srv.end();
    }
}

class EchoTcpServer extends Thread {
    private int port;
    private boolean running;

    public EchoTcpServer(int port) {
        this.port = port;
    }

    public void run() {
        try (ServerSocket serverSocket = new ServerSocket(this.port)) {
            running = true;
            while (running) {
                Socket clientSocket = serverSocket.accept();
                try (PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
                        BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));) {
                    String greeting = in.readLine();
                    if ("hello tcp server".equals(greeting)) {
                        out.println("hello tcp client");
                    } else {
                        out.println("unrecognized greeting");
                    }
                }
            }
        } catch (

        IOException e) {
            System.err.print("from run ");
            System.err.println(e);
        }
    }

    public void end() {
        running = false;
    }
}