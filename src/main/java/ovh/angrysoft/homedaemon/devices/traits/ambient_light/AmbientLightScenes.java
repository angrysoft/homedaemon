package ovh.angrysoft.homedaemon.devices.traits.ambient_light;

import ovh.angrysoft.homedaemon.devices.traits.Trait;

public interface AmbientLightScenes extends Trait{
    void setScene(String sceneName);
}
