package ovh.angrysoft.homedaemon.watcher;

import java.util.HashMap;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class WatcherManager  implements WatcherHandler {
    private HashMap<String, Watcher> watchers;
    private DeviceManager deviceManager;
    
    public WatcherManager(DeviceManager deviceManager) {
        this.watchers = new HashMap<>();
        this.deviceManager = deviceManager;
    }

    public boolean isRegistered(String sid) {
        return this.watchers.containsKey(sid);
    }

    public void registerWatcher(Watcher watcher) {
        assert watchers.containsKey(watcher.getSid()) == false : "Watcher is registered";
        watcher.setHandler(this);
        watchers.put(watcher.getSid(), watcher);
        watcher.start();
    }

    public void call(StatusEvent message) {
        deviceManager.update(message);
    }
}