package ovh.angrysoft.homedaemon.io;

import ovh.angrysoft.homedaemon.bus.EventBus;

public class IOManager {
    EventBus bus;
    private String ioPackage = "ovh.angrysoft.homedaemon.io";
    private String[] ioList;

    public IOManager(String[] ioList, EventBus bus) {
        this.bus = bus;
        this.ioList = ioList;
    }

    public void loadIO() {
        for (String ioName : ioList) {
            StringBuilder ioPathBuilder = new StringBuilder(ioPackage);
            ioPathBuilder.append(".")
                    .append(ioName);
            loadIoClass(ioName);
        }
    }

    private void loadIoClass(String ioPath) {
        System.out.println(ioPath);
    }
}
