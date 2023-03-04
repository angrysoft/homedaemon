package ovh.angrysoft.homedaemon.traits;

public interface OnOff extends Trait {
    void on();
    void off();
    boolean isOn();
    boolean isOff();
    
}
