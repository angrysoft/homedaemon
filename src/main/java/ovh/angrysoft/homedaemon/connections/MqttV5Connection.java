package ovh.angrysoft.homedaemon.connections;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.BiConsumer;
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

import ovh.angrysoft.homedaemon.devices.xiaomi.aqara.Plug;

public class MqttV5Connection extends Thread implements MqttCallback {
    // MQTT broker URI to connect to. Defaults to tcp://iot.eclipse.org:1883. Use
    // ws:// for Websockets, wss:// for secure Websockets and ssl:// for TLS
    // encrypted TCP connections.");
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");

    private String clientId;
    private int qos;
    protected int timeout;
    private MqttConnectionOptions connOpts = new MqttConnectionOptions();
    private MqttAsyncClient client;
    final Thread mainThread = Thread.currentThread();
    static volatile boolean keepRunning = true;
    private List<String> topics;
    private BiConsumer<String, String> onMsgHandler;

    private void setUri(String uri) {
        this.connOpts.setServerURIs(new String[] { uri });
    }

    private void setUser(String user) {
        this.connOpts.setUserName(user);
    }

    private void setPassword(String password) {
        this.connOpts.setPassword(password.getBytes());
    }

    private void setAutomaticReconnect(boolean isAutoRec) {
        this.connOpts.setAutomaticReconnect(isAutoRec);
    }

    private void setKeepAlive(int keepAlive) {
        this.connOpts.setKeepAliveInterval(timeout);
    }

    private MqttV5Connection() {
        this.connOpts = new MqttConnectionOptions();
        this.qos = 0;
        this.topics = new ArrayList<String>();
    }

    public static final class Builder {
        private String uri;
        private Optional<String> user;
        private Optional<String> password;
        private Optional<Boolean> autoReconnect;
        private int keepAlive = 5000;
        private int timeout = 5000;
        private String clientId;

        public Builder uri(String uri) {
            this.uri = uri;
            return this;
        }

        public Builder user(String user) {
            this.user = Optional.of(user);
            return this;
        }

        public Builder password(String password) {
            this.password = Optional.of(password);
            return this;
        }

        public Builder autoReconnect(Boolean autoRec) {
            this.autoReconnect = Optional.of(autoRec);
            return this;
        }

        public Builder keepAlive(int keepAlive) {
            this.keepAlive = keepAlive;
            return this;
        }

        public Builder timeout(int timeout) {
            this.timeout = timeout;
            return this;
        }

        public Builder clientId(String clientId) {
            this.clientId = clientId;
            return this;
        }

        public MqttV5Connection build() {
            MqttV5Connection mqttConn = new MqttV5Connection();
            mqttConn.setUri(uri);
            this.user.ifPresent(mqttConn::setUser);
            this.password.ifPresent(mqttConn::setPassword);
            this.autoReconnect.ifPresent(mqttConn::setAutomaticReconnect);
            mqttConn.timeout = timeout;
            mqttConn.setKeepAlive(keepAlive);
            if (clientId == null || clientId.isEmpty()) {
                long pid = Thread.currentThread().getId();
                clientId = "homedaemon-client" + pid;
            }
            mqttConn.clientId = clientId;
            return mqttConn;
        }

    }

    public static Builder builder() {
        return new Builder();
    }

    public synchronized void addTopic(String topic) {
        this.topics.add(topic);
        if (isConnected()) {
            try {
                this.client.subscribe(topic, this.qos);
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

    public synchronized void removeTopic(String topic) {
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

    public void run() {

        MemoryPersistence persistence = new MemoryPersistence();
        try {
            this.client = new MqttAsyncClient(this.getUris()[0], this.getClientId(), persistence);
            this.client.setCallback(this);
            IMqttToken connectToken = this.client.connect(this.connOpts);
            connectToken.waitForCompletion(this.timeout);
            subscribe();
        } catch (MqttException e) {
            e.printStackTrace();
        }
        System.err.println(String.format("from run Watcher %s - %s", Thread.currentThread(), mainThread));
    }

    private void subscribe() {
        try {
            for (String topic : this.topics) {
                IMqttToken subToken = this.client.subscribe(topic, this.qos);
                subToken.waitForCompletion(timeout);
            }
        } catch (MqttException e) {
            LOGGER.log(Level.ALL, "Mqtt subscribe: {0}", e.getMessage());
        }
    }

    public void publishMessage(byte[] payload, int qos, boolean retain, String topic)
            throws MqttPersistenceException, MqttException {
        if (!isConnected()) {
            LOGGER.warning("Not Connected");
            return;
        }
        MqttMessage message = new MqttMessage(payload);
        message.setQos(qos);
        message.setRetained(retain);
        IMqttToken deliveryToken = client.publish(topic, message);
        deliveryToken.waitForCompletion(this.timeout);
    }

    public void setOnMsgHandler(BiConsumer<String, String> onMsgHandler) {
        this.onMsgHandler = onMsgHandler;
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
            LOGGER.severe(String.format("Mqtt client exit with: %s", e.getMessage()));
        }

    }

    public String[] getUris() {
        return this.connOpts.getServerURIs();
    }

    public String getClientId() {
        return clientId;
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
        if (this.onMsgHandler != null) {
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

    private boolean isConnected() {
        if (client != null && client.isConnected())
            return true;
        return false;
    }
}
