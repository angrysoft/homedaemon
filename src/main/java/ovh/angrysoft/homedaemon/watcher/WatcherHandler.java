package ovh.angrysoft.homedaemon.watcher;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;

public interface WatcherHandler {
    void call(StatusEvent message);
}
