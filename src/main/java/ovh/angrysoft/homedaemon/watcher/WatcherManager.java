package ovh.angrysoft.homedaemon.watcher;

import java.util.ArrayList;

import ovh.angrysoft.homedaemon.bus.EventBus;

public class WatcherManager  implements WatcherHandler {
    private ArrayList<Watcher> watchers;
    private EventBus bus;
    
    public WatcherManager(EventBus bus) {
        this.watchers = new ArrayList<>();
        this.bus = bus;
    }

    public void registerWatcher(Watcher watcher) {
        watcher.setHandler(this);
        watchers.add(watcher);
        watcher.start();
    }

    public void call(StatusMessage message) {
        System.out.println(message);
        //TODO device update status if change call bus.dispatch
    }
}
