package ovh.angrysoft.homedaemon.connections;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.eclipse.paho.mqttv5.client.IMqttToken;
import org.eclipse.paho.mqttv5.client.MqttAsyncClient;
import org.eclipse.paho.mqttv5.client.MqttCallback;
import org.eclipse.paho.mqttv5.client.MqttConnectionOptions;
import org.eclipse.paho.mqttv5.client.MqttDisconnectResponse;
import org.eclipse.paho.mqttv5.client.persist.MemoryPersistence;
import org.eclipse.paho.mqttv5.common.MqttException;
import org.eclipse.paho.mqttv5.common.MqttMessage;
import org.eclipse.paho.mqttv5.common.packet.MqttProperties;

public class MqttV5Connection implements MqttCallback {
    // MQTT broker URI to connect to. Defaults to tcp://iot.eclipse.org:1883. Use
    // ws:// for Websockets, wss:// for secure Websockets and ssl:// for TLS
    // encrypted TCP connections.");
    private String hostURI;
    private String user;
    private String password;
    private String clientID;
    private int timeout;
    private boolean autoReconnect = false;
    private MqttConnectionOptions connOpts = new MqttConnectionOptions();
    private MqttAsyncClient client;
    final Thread mainThread = Thread.currentThread();
    static volatile boolean keepRunning = true;
    private List<String> topics;

    public MqttV5Connection(HashMap<String, Object> config) {
        this.connOpts = new MqttConnectionOptions();
        if (config.containsKey("host")) {
            this.hostURI = (String) config.get("host");
            this.connOpts.setServerURIs(new String[] { this.hostURI });
        }

        if (config.containsKey("user")) {
            this.user = (String) config.get("user");
            this.connOpts.setUserName(this.user);
        }

        if (config.containsKey("password")) {
            this.password = (String) config.get("password");
            this.connOpts.setPassword(this.password.getBytes());
        }

        if (config.containsKey("autoReconnect")) {
            this.autoReconnect = (boolean) config.get("autoReconnect");
            this.connOpts.setAutomaticReconnect(this.autoReconnect);
        }

        // if (cliOptions.hasOption("will-payload") &&
        // cliOptions.hasOption("will-topic")) {
        // String willPayload = cliOptions.getOptionValue("will-payload");
        // String willTopic = cliOptions.getOptionValue("will-topic");
        // int qos = 0;
        // boolean retained = false;
        // if (cliOptions.hasOption("will-qos")) {
        // qos = Integer.parseInt(cliOptions.getOptionValue("will-qos"));
        // }
        // if (cliOptions.hasOption("will-retain")) {
        // retained = true;
        // }
        // MqttMessage willMessage = new MqttMessage(willPayload.getBytes(), qos,
        // retained, null);
        // conOpts.setWill(willTopic, willMessage);
        // }

        this.topics = new ArrayList<String>();

        this.timeout = 5000;

        if (clientID == null || clientID == "") {
            // No client ID provided, generate one from the process ID
            long pid = Thread.currentThread().getId(); // ProcessHandle.current().pid();
            clientID = "mqtt-client-" + pid;
        }

    }

    public void addTopic(String topic) {
        this.topics.add(topic);
    }

    public void connect() {
        MemoryPersistence persistence = new MemoryPersistence();
        try {
            this.client = new MqttAsyncClient(this.getHostURI(), this.getClientID(), persistence);
            this.client.setCallback(this);
            IMqttToken connectToken = client.connect(this.getconnOpts());
            connectToken.waitForCompletion(timeout);
            IMqttToken subToken = this.client.subscribe("test1/dupa", 0);
            subToken.waitForCompletion(timeout);
            addShutdownHook();
            while (keepRunning) {
                // Do nothing
            }
            disconnectClient();
            closeClientAndExit();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void addShutdownHook() {

        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                keepRunning = false;
            }
        });
    }

    private void disconnectClient() throws MqttException {
        // Disconnect
        System.out.println("Disconnecting from server.");
        IMqttToken disconnectToken = client.disconnect();
        disconnectToken.waitForCompletion(this.timeout);
    }

    private void closeClientAndExit() {
        // Close the client
        System.out.println("Closing Connection.");
        try {
            this.client.close();
            System.out.println("Client Closed.");
            System.exit(0);
            mainThread.join();
        } catch (MqttException | InterruptedException e) {
            // End the Application
            System.exit(1);
        }

    }

    public String getHostURI() {
        return hostURI;
    }

    public String getClientID() {
        return clientID;
    }

    public MqttConnectionOptions getconnOpts() {
        return connOpts;
    }

    @Override
    public void disconnected(MqttDisconnectResponse disconnectResponse) {
        String cause = null;
        if (disconnectResponse.getException().getMessage() != null) {
            cause = disconnectResponse.getException().getMessage();
        } else {
            cause = disconnectResponse.getReasonString();
        }
        System.out.println(
                String.format("The connection to the server was lost, cause: %s. Waiting to reconnect.", cause));
    }

    @Override
    public void mqttErrorOccurred(MqttException exception) {
        System.err.println(String.format("An MQTT error occurred: %s", exception.getMessage()));
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        String messageContent = new String(message.getPayload());

        System.out.println(messageContent);
    }

    @Override
    public void deliveryComplete(IMqttToken token) {
        System.out.println(String.format("Message %d was delivered.", token.getMessageId()));
    }

    @Override
    public void connectComplete(boolean reconnect, String serverURI) {
        System.out.println(String.format("Connection to %s complete. Reconnect=%b", serverURI, reconnect));
    }

    @Override
    public void authPacketArrived(int reasonCode, MqttProperties properties) {
        System.out.println(
                String.format("Auth packet received, this client does not currently support them. Reason Code: %d.",
                        reasonCode));
    }
}
