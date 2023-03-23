package ovh.angrysoft.homedaemon.devices;

public interface Gateway {
    void send(String sid, String msg);
    void registerSubDevice(String sid, String model);
}
