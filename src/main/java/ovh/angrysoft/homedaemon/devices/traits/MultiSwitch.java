package ovh.angrysoft.homedaemon.devices.traits;

public interface MultiSwitch extends Trait {
    void on(String switchName);
    void off(String switchName);
    boolean isOn(String switchName);
    boolean isOff(String switchName);
    boolean toggle(String switchName);
}
