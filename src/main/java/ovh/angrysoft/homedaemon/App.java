package ovh.angrysoft.homedaemon;


import ovh.angrysoft.homedaemon.devices.Manager;
import ovh.angrysoft.homedaemon.watcher.YeelightWatcher;

public class App {
    public static void main(String[] args) {
        String devDir = System.getenv("DEVDIR");
        // String confDir = System.getenv("CONFDIR");
        System.out.println(devDir);
        // System.out.println(confDir);
        Manager manger = new Manager(devDir);
        manger.loadDevice();
        manger.setup();
        YeelightWatcher watcher = new YeelightWatcher("192.168.10.27", 55443);
        watcher.start();
    }
}
