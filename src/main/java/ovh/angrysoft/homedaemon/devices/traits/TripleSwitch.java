package ovh.angrysoft.homedaemon.devices.traits;

public interface TripleSwitch extends DoubleSwitch {
    void three(Boolean state);

    boolean isThreeOn();

    void toggleThree();
}
