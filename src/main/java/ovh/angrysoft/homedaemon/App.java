package ovh.angrysoft.homedaemon;


import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.devices.Manager;
import ovh.angrysoft.homedaemon.watcher.WatcherManager;
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
        EventBus bus = new EventBus();
        WatcherManager wm = new WatcherManager(bus);
        wm.registerWatcher(new YeelightWatcher("0x0000000007200259", "192.168.10.27", 55443));
        // YeelightWatcher watcher = 
        // watcher.start();
    }
}
