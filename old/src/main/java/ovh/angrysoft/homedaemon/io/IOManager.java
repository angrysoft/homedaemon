package ovh.angrysoft.homedaemon.io;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.config.Config;
import ovh.angrysoft.homedaemon.config.HomedConfig;

public class IOManager {
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");
    EventBus bus;
    Config config;
    private String ioPackage = "ovh.angrysoft.homedaemon.io";
    private List<BaseIo> ios;

    public IOManager(Config config, EventBus bus) {
        this.bus = bus;
        this.config = config;
        this.ios = new ArrayList<>();
    }

    public void loadIO() {
        HomedConfig homedConfig = (HomedConfig) config.get("homed");
        for (String ioName : homedConfig.io()) {
            String ioPath = new StringBuilder(ioPackage)
                    .append(".")
                    .append(ioName)
                    .toString();
            loadIoClass(ioPath);
        }
    }

    private void loadIoClass(String ioPath) {
        try {
            LOGGER.info(String.format("Load io module: %s", ioPath));
            Class<?> io = Class.forName(ioPath);
            Constructor<?> ioConstructor = io.getConstructors()[0];
            BaseIo ioInstance = (BaseIo) ioConstructor.newInstance(config, bus);
            ioInstance.start();
            this.addIo(ioInstance);
        } catch (InstantiationException | IllegalAccessException | IllegalArgumentException
                | InvocationTargetException | ClassNotFoundException e) {
            LOGGER.warning(new StringBuilder(ioPath).append(" ").append(e.getCause()).toString());
        }
    }

    private synchronized void addIo(BaseIo io) {
        this.ios.add(io);
    }
}
