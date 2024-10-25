package ovh.angrysoft.homedaemon.devices.traits.ambient_light;

import ovh.angrysoft.homedaemon.devices.traits.Trait;

public interface AmbientLight extends Trait {
    void ambientLightState(Boolean state);

    void ambientLightToggle();

    boolean isAmbientLightOn();
}
