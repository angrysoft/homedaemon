package ovh.angrysoft.homedaemon.watcher;

import java.util.HashMap;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.devices.HomedaemonDeviceManager;

public class WatcherManager implements WatcherHandler {
    private HashMap<String, Watcher> watchers;
    private HomedaemonDeviceManager deviceManager;

    public WatcherManager(HomedaemonDeviceManager deviceManager) {
        this.watchers = new HashMap<>();
        this.deviceManager = deviceManager;
    }

    public boolean isRegistered(String sid) {
        return this.watchers.containsKey(sid);
    }

    public void registerWatcher(Watcher watcher) {
        if (watchers.containsKey(watcher.getSid())) {
            return;
        }
        watcher.setHandler(this);
        watchers.put(watcher.getSid(), watcher);
        watcher.start();
    }

    public void call(StatusEvent message) {
        deviceManager.update(message);
    }
}
