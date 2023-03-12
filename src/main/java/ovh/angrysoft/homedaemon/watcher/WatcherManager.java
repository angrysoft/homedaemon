package ovh.angrysoft.homedaemon.watcher;

import java.util.ArrayList;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class WatcherManager  implements WatcherHandler {
    private ArrayList<Watcher> watchers;
    private DeviceManager deviceManager;
    
    public WatcherManager(DeviceManager deviceManager) {
        this.watchers = new ArrayList<>();
        this.deviceManager = deviceManager;
    }

    public void registerWatcher(Watcher watcher) {
        watcher.setHandler(this);
        watchers.add(watcher);
        watcher.start();
    }

    public void call(StatusEvent message) {
        deviceManager.update(message);
    }
}
