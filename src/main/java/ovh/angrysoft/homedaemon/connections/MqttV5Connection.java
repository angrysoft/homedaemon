package ovh.angrysoft.homedaemon.connections;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.eclipse.paho.mqttv5.client.IMqttToken;
import org.eclipse.paho.mqttv5.client.MqttAsyncClient;
import org.eclipse.paho.mqttv5.client.MqttCallback;
import org.eclipse.paho.mqttv5.client.MqttConnectionOptions;
import org.eclipse.paho.mqttv5.client.MqttDisconnectResponse;
import org.eclipse.paho.mqttv5.client.persist.MemoryPersistence;
import org.eclipse.paho.mqttv5.common.MqttException;
import org.eclipse.paho.mqttv5.common.MqttMessage;
import org.eclipse.paho.mqttv5.common.MqttPersistenceException;
import org.eclipse.paho.mqttv5.common.packet.MqttProperties;

public class MqttV5Connection implements MqttCallback {
    // MQTT broker URI to connect to. Defaults to tcp://iot.eclipse.org:1883. Use
    // ws:// for Websockets, wss:// for secure Websockets and ssl:// for TLS
    // encrypted TCP connections.");
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");
    private String uri;
    private String user;
    private String password;
    private String clientID;
    private int timeout;
    private int qos;
    private boolean autoReconnect = false;
    private MqttConnectionOptions connOpts = new MqttConnectionOptions();
    private MqttAsyncClient client;
    final Thread mainThread = Thread.currentThread();
    static volatile boolean keepRunning = true;
    private List<String> topics;
    private BiConsumer<String,String> onMsgHandler;

    public MqttV5Connection(Map<String, String> config) {

        this.connOpts = new MqttConnectionOptions();
        if (config.containsKey("uri")) {
            this.uri = config.get("uri");
            this.connOpts.setServerURIs(new String[] { this.uri });
        }

        if (config.containsKey("user")) {
            this.user = config.get("user");
            this.connOpts.setUserName(this.user);
        }

        if (config.containsKey("password")) {
            this.password = config.get("password");
            this.connOpts.setPassword(this.password.getBytes());
        }

        if (config.containsKey("autoReconnect")) {
            this.autoReconnect = Boolean.parseBoolean(config.get("autoReconnect"));
            this.connOpts.setAutomaticReconnect(this.autoReconnect);
        }

        this.timeout = 5000;
        if (config.containsKey("timeout")) {
            this.timeout = Integer.parseInt(config.get("timeout"));
        }
        this.connOpts.setKeepAliveInterval(this.timeout);

        this.qos = 0;

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

        if (clientID == null || clientID == "") {
            long pid = Thread.currentThread().getId();
            clientID = "homedaemon-client" + pid;
        }

    }

    public void addTopic(String topic) {
        this.topics.add(topic);
        if (this.client.isConnected()) {
            try {
                this.client.subscribe(topic, this.qos);
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

    public void removeTopic(String topic) {
        this.topics.remove(topic);
        if (this.client.isConnected()) {
            try {
                this.client.unsubscribe(topic);
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

    public List<String> getTopics() {
        return topics;
    }

    public void connect() {
        MemoryPersistence persistence = new MemoryPersistence();
        LOGGER.info("Try to connect");
        try {
            this.client = new MqttAsyncClient(this.getUri(), this.getClientID(), persistence);
            this.client.setCallback(this);
            IMqttToken connectToken = this.client.connect(this.connOpts);
            connectToken.waitForCompletion(this.timeout);
            subscribe();
            addShutdownHook();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    private void subscribe() {
        try {
            for (String topic : this.topics) {
                IMqttToken subToken = this.client.subscribe(topic, 0);
                subToken.waitForCompletion(timeout);
            }
        } catch (MqttException e) {
            LOGGER.log(Level.ALL, "Mqtt subscribe: {0}", e.getMessage());
        }
    }

    public void publishMessage(byte[] payload, int qos, boolean retain, String topic)
            throws MqttPersistenceException, MqttException {
        MqttMessage message = new MqttMessage(payload);
        message.setQos(qos);
        message.setRetained(retain);
        IMqttToken deliveryToken = client.publish(topic, message);
        deliveryToken.waitForCompletion(this.timeout);
    }

    public void setOnMsgHandler(BiConsumer<String, String> onMsgHandler) {
        this.onMsgHandler = onMsgHandler;
    }

    public void addShutdownHook() {

        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                keepRunning = false;
            }
        });
    }

    public void disconnect() throws MqttException {
        LOGGER.info("Disconnecting from server.");
        IMqttToken disconnectToken = client.disconnect();
        disconnectToken.waitForCompletion(this.timeout);

        LOGGER.info("Closing Connection.");
        try {
            this.client.close();
            LOGGER.info("Client Closed.");
            mainThread.join();
        } catch (MqttException | InterruptedException e) {
            LOGGER.log(Level.ALL, "Mqtt client exit with: {0}", e.getMessage());
        }

    }

    public String getUri() {
        return uri;
    }

    public String getClientID() {
        return clientID;
    }

    public MqttConnectionOptions getConnOpts() {
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
        LOGGER.log(Level.FINE,
                String.format("The connection to the server was lost, cause: %s. Waiting to reconnect.", cause));
    }

    @Override
    public void mqttErrorOccurred(MqttException exception) {
        LOGGER.log(Level.ALL, String.format("An MQTT error occurred: %s", exception.getMessage()));
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        String messageContent = new String(message.getPayload());
        if (this.onMsgHandler == null) {
            this.onMsgHandler.accept(topic, messageContent);
            return;
        }
        LOGGER.info(messageContent);
        
    }

    @Override
    public void deliveryComplete(IMqttToken token) {
        LOGGER.fine(String.format("Message %d was delivered.", token.getMessageId()));
    }

    @Override
    public void connectComplete(boolean reconnect, String serverURI) {
        LOGGER.info(String.format("Connection to %s complete. Reconnect=%b", serverURI, reconnect));
    }

    @Override
    public void authPacketArrived(int reasonCode, MqttProperties properties) {
        LOGGER.warning(
                String.format("Auth packet received, this client does not currently support them. Reason Code: %d.",
                        reasonCode));
    }
}
