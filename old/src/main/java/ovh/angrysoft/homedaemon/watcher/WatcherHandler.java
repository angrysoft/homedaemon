package ovh.angrysoft.homedaemon.watcher;

import ovh.angrysoft.homedaemon.bus.Event;

public interface WatcherHandler {
    void call(Event message);
}
