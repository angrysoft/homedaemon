package ovh.angrysoft.homedaemon.devices;

public interface ZigbeeGateway {
    void sendSet(String sid, String cmd, Object value);
    void sendGet(String sid, String cmd, Object value);

    void registerSubDevice(String sid, String model);
}
