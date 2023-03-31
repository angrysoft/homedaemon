package ovh.angrysoft.homedaemon.devices.traits;

public interface Dimmer extends Trait {
    void setBright(Integer value);
    int getBright();
}

