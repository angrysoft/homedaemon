package ovh.angrysoft.homedaemon.devices.traits;

public interface TripleSwitch extends DoubleSwitch {
    void center(Boolean state);

    boolean isCenterOn();

    void toggleCenter();
}
