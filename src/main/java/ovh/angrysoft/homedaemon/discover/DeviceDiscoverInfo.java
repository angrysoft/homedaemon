package ovh.angrysoft.homedaemon.discover;

public interface DeviceDiscoverInfo {
    public String getDeviceSid();

    public <T> T get(String key);

    public boolean containsKey(String key);
}
