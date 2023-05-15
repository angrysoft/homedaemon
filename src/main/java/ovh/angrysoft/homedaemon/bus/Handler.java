package ovh.angrysoft.homedaemon.bus;

public interface Handler {
    public void call(Event event);
}
