package ovh.angrysoft.homedaemon.devices.traits.backlight;

import ovh.angrysoft.homedaemon.devices.traits.Trait;

public interface Backlight extends Trait {
    void backlightState(boolean state);
    void backlightToggle();
    boolean isBacklightOn();
}
