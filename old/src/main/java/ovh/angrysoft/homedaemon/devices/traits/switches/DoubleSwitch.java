package ovh.angrysoft.homedaemon.devices.traits.switches;

import ovh.angrysoft.homedaemon.devices.traits.Trait;

public interface DoubleSwitch extends Trait {
    void outlet0(Boolean state);

    void outlet1(Boolean state);

    boolean isOutlet0On();

    boolean isOutlet1On();

    void toggleOutlet0();

    void toggleOutlet1();

    void allOn();

    void allOff();
}
