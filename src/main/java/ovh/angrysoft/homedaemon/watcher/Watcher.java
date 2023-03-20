package ovh.angrysoft.homedaemon.watcher;

public abstract class Watcher extends Thread {
    protected String sid;

    public Watcher(String sid) {
        this.sid = sid;
    }

    public String getSid() {
        return sid;
    }

    public WatcherHandler handler;
    public abstract void run();
    public void setHandler(WatcherHandler handler) {
        this.handler = handler;
    }


}
