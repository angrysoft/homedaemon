package ovh.angrysoft.homedaemon.io;

import ovh.angrysoft.homedaemon.bus.EventBus;

public class IOManager {
    EventBus bus;
    private String ioPackage = "ovh.angrysoft.homedaemon.io";


    public IOManager(String[] ioList, EventBus bus) {
        this.bus = bus;
    }

    public void loadIO() {

    }
}
