package ovh.angrysoft.homedaemon.watcher;

public abstract class Watcher extends Thread {
    protected String sid;
    protected WatcherHandler handler;

    public Watcher(String sid) {
        this.sid = sid;
    }

    public String getSid() {
        return sid;
    }

    public abstract void run();

    public void setHandler(WatcherHandler handler) {
        this.handler = handler;
    }

    public WatcherHandler getHandler() {
        return handler;
    }

}
