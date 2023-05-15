package ovh.angrysoft.homedaemon.devices;

public interface Gateway {
    void sendSet(String sid, String cmd, Object value);

    void sendGet(String sid, String cmd, Object value);

    void registerSubDevice(String sid, String model);
}
