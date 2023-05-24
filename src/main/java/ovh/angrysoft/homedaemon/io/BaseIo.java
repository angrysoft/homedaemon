package ovh.angrysoft.homedaemon.io;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.config.Config;

public abstract class BaseIo {
    protected Config config;
    protected EventBus bus;

    public BaseIo(Config config, EventBus bus) {
        this.config = config;
        this.bus = bus;
    }

    public abstract void run();
}
