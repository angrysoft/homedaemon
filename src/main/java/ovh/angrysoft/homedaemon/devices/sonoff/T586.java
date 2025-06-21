package ovh.angrysoft.homedaemon.devices.sonoff;

import java.util.List;
import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.ambient_light.AmbientLight;
import ovh.angrysoft.homedaemon.devices.traits.ambient_light.AmbientLightScenes;
import ovh.angrysoft.homedaemon.discover.engines.EwelinkDiscoverEngine;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.watcher.EwelinkWatcher;

public class T586 extends BaseDevice implements AmbientLight, AmbientLightScenes {
    EwelinkApi api;

    public T586(DeviceInfo deviceInfo) {
        super(deviceInfo);
        this.discoverable = true;
        this.discoverEngine = new EwelinkDiscoverEngine();
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("ip", "localhost"));
            this.status.registerAttribute(new DeviceAttribute<Integer>("port", 0));
            this.status.registerAttribute(new DeviceAttribute<String>("ambientLight", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("ambientLightScene", -1));
            this.status.registerAttribute(new DeviceAttribute<String>("startup", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("pulse", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("pulseWidth", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("rrsi", ""));
            this.status.registerAttribute(new DeviceAttribute<String>("ssid", ""));
            this.status.registerAttribute(new DeviceAttribute<Integer>("shock", -1));
            this.status.registerAttribute(
                    new DeviceAttribute<List<String>>("ambientLightSceneList", List.of("Night Light", "Party",
                            "Leisure", "Color", "Childhood", "Wiper", "Fairy", "Starburst"), true));
            this.status.registerAttribute(
                    new DeviceAttribute<String>("token", deviceInfo.getArgs().get("token")));
        } catch (AttributeAlreadyExist e) {
            logger.warning(e.getMessage());
        }
    }

    @Override
    public void setup() {
        this.api =
                new EwelinkApi(status.get("ip"), status.get("port"), getSid(), status.get("token"));
        this.watcher = EwelinkWatcher.getInstance();
        EwelinkWatcher.registerDevice(getSid(), status.get("token"));
    }

    @Override
    public void ambientLightState(Boolean state) {
        api.setLightSwitch(state);
    }

    @Override
    public boolean isAmbientLightOn() {
        return ((String) status.get("ambientLight")).equalsIgnoreCase("on");
    }

    @Override
    public void ambientLightToggle() {
        ambientLightState(!isAmbientLightOn());
    }

    @Override
    public void setScene(String sceneName) {
        List<String> scenes = status.get("ambientLightSceneList");
        if (scenes.contains(sceneName))
            api.setLightMode(scenes.indexOf(sceneName));
    }

}
