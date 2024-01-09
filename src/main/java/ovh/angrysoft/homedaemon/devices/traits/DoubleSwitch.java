package ovh.angrysoft.homedaemon.devices.traits;

public interface DoubleSwitch extends Trait {
    void one(Boolean state);

    void two(Boolean state);

    boolean isOneOn();

    boolean isTwoOn();

    void toggleOne();

    void toggleTwo();

    void allOn();

    void allOff();
}
