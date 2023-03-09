package ovh.angrysoft.homedaemon.devices.traits;

public interface OnOff extends Trait {
    void on();
    void off();
    boolean isOn();
    
}
