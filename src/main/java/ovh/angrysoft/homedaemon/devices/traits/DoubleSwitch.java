package ovh.angrysoft.homedaemon.devices.traits;

public interface DoubleSwitch extends Trait {
    void left(boolean state);
    void right(boolean state);
    boolean isLeftOn();
    boolean isRightOn();
    void toggleLeft();
    void toggleRight();
}
