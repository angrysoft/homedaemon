package ovh.angrysoft.homedaemon.devices.traits;

public interface DoubleSwitch extends Trait {
    void left(Boolean state);
    void right(Boolean state);
    boolean isLeftOn();
    boolean isRightOn();
    void toggleLeft();
    void toggleRight();
    void allOn();
    void allOff();
}
