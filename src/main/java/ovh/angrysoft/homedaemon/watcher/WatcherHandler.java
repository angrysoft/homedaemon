package ovh.angrysoft.homedaemon.watcher;

public interface WatcherHandler {
    void call(StatusMessage message);
}
