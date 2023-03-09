package ovh.angrysoft.homedaemon.watcher;

import java.util.ArrayList;

public class WatcherManager {
    private ArrayList<Watcher> watchers;
    
    public WatcherManager() {
        this.watchers = new ArrayList<>();
    }

    public void registerWatcher(Watcher watcher) {
        watchers.add(watcher);
        watcher.start();
    }
}
