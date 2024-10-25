package ovh.angrysoft.homedaemon.io;

import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.config.Config;

public abstract class BaseIo extends Thread {
    protected final Logger LOGGER = Logger.getLogger("Homedaemon");
    protected Config config;
    protected EventBus bus;

    public BaseIo(Config config, EventBus bus) {
        this.config = config;
        this.bus = bus;
    }

    public abstract void run();
}
