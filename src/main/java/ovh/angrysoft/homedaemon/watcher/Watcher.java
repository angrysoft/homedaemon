package ovh.angrysoft.homedaemon.watcher;

public abstract class Watcher extends Thread {
    protected String sid;
    protected WatcherHandler handler;

    Watcher(String sid) {
        this.sid = sid;
    }

    public String getSid() {
        return sid;
    }

    public void setHandler(WatcherHandler handler) {
        this.handler = handler;
    }

    @Override
    public abstract void run();

    public WatcherHandler getHandler() {
        return handler;
    }

}
