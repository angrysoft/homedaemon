package ovh.angrysoft.homedaemon.devices.traits.switches;

public interface TripleSwitch extends DoubleSwitch {
    void outlet2(Boolean state);

    boolean isOutlet2On();

    void toggleOutlet2();
}
