package ovh.angrysoft.homedaemon.watcher;

import ovh.angrysoft.homedaemon.bus.Events.DeviceEvent;

public interface WatcherHandler {
    void call(DeviceEvent message);
}
