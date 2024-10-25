package ovh.angrysoft.homedaemon.devices.traits;

public interface Brightness extends Trait {
    void setBright(Integer value);
    int getBright();
}

