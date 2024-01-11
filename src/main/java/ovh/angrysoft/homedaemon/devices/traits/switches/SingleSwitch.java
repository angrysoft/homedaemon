package ovh.angrysoft.homedaemon.devices.traits.switches;

import ovh.angrysoft.homedaemon.devices.traits.Trait;

public interface SingleSwitch extends Trait {
    void outlet(Boolean state);

    boolean isOutletOn();

    void toggleOutlet();

    void allOn();

    void allOff();
}
