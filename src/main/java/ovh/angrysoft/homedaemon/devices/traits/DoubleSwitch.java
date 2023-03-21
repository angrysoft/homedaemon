package ovh.angrysoft.homedaemon.devices.traits;

public interface DoubleSwitch extends Trait {
    void left(boolean status);
    void right(boolean status);
    boolean isLeftOn();
    boolean isRightOn();
    boolean toggleLeft();
    boolean toggleRight();
}
