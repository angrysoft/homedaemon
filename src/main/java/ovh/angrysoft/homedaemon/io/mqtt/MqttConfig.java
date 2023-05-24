package ovh.angrysoft.homedaemon.io.mqtt;

public record MqttConfig(String addr, Integer port, boolean ssl, String user, String password) {

}
