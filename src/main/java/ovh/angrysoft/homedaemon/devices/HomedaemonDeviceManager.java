package ovh.angrysoft.homedaemon.devices;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceInitError;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceNotSupported;
import ovh.angrysoft.homedaemon.exceptions.devices.GatewayNotFound;
import ovh.angrysoft.homedaemon.watcher.Watcher;
import ovh.angrysoft.homedaemon.watcher.WatcherManager;

public class HomedaemonDeviceManager implements DeviceManager {
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");
    private String deviceInfoDir;
    private List<DeviceInfo> devicesInfoList;
    private EventBus bus;
    private Map<String, BaseDevice> devices;
    private Map<String, Class<?>> drivers;
    private WatcherManager watcherManager;
    private String driverPackage = "ovh.angrysoft.homedaemon.devices";

    public HomedaemonDeviceManager(String deviceInfoDir, EventBus bus) {
        this.deviceInfoDir = deviceInfoDir;
        this.devicesInfoList = new ArrayList<DeviceInfo>();
        this.bus = bus;
        this.devices = new HashMap<>();
        this.drivers = new HashMap<>();
        this.watcherManager = new WatcherManager(this);
    }

    public WatcherManager getWatcherManager() {
        return watcherManager;
    }

    public void loadDeviceInfo() {
        setupInternalDevicesInfo();

        File devDir = new File(deviceInfoDir);
        if (!devDir.exists() && !devDir.isDirectory()) {
            LOGGER.log(Level.ALL, "Cannot access device dir : {0}", deviceInfoDir);
            return;
        }

        for (File devInfoFile : devDir.listFiles((File file) -> {
            if (file.getName().endsWith(".json"))
                return true;
            return false;
        })) {
            try {

                DeviceInfo deviceInfo = new Gson().fromJson(new FileReader(devInfoFile), DeviceInfo.class);
                deviceInfo.checkFields();

                String devType = deviceInfo.getType();
                if (devType == null || devicesInfoList.contains(deviceInfo))
                    continue;

                if (devType.equals("gateway")) {
                    devicesInfoList.add(0, deviceInfo);
                    continue;
                }
                devicesInfoList.add(deviceInfo);

            } catch (FileNotFoundException e) {
                LOGGER.log(Level.SEVERE, "Device info file {0} not found", devInfoFile.getName());
            } catch (JsonSyntaxException e) {
                LOGGER.log(Level.SEVERE, "Device info file parse error: {0}", devInfoFile.getName());
            } catch (VerifyError e) {
                LOGGER.log(Level.SEVERE,
                        String.format("Device info file parse error: %s : %s", devInfoFile.getName(), e.getMessage()));
            }
        }
    }

    private void setupInternalDevicesInfo() {
        // Clock
        Map<String, String> clockName = new HashMap<>();
        clockName.put("pl", "Zegar");
        clockName.put("en", "Clock");
        Map<String, String> clockPlace = new HashMap<>();
        clockPlace.put("pl", "Wszędzie");
        clockPlace.put("en", "everywhere");
        DeviceInfo clockInfo = new DeviceInfo(
                "clock",
                "clock",
                "homedaemon",
                "clock",
                clockName,
                clockPlace,
                "software.ClockDevice",
                new HashMap<>());
        this.devicesInfoList.add(clockInfo);

        // State
        Map<String, String> stateName = new HashMap<>();
        clockName.put("pl", "Stan");
        clockName.put("en", "State");
        Map<String, String> statePlace = new HashMap<>();
        clockPlace.put("pl", "Wszędzie");
        clockPlace.put("en", "everywhere");
        DeviceInfo stateInfo = new DeviceInfo(
                "state",
                "state",
                "homedaemon",
                "state",
                stateName,
                statePlace,
                "software.StateDevice",
                new HashMap<>());
        this.devicesInfoList.add(stateInfo);
    }

    public void setupDevices() {
        for (DeviceInfo devInfo : devicesInfoList) {
            LOGGER.log(Level.INFO, String.format("load device: %s model : %s", devInfo.getSid(), devInfo.getModel()));
            try {
                Class<?> driver = getDriver(devInfo.getDriver());
                BaseDevice device = initDevice(driver, devInfo);
                Watcher deviceWatcher = device.getWatcher();
                if (deviceWatcher != null) {
                    watcherManager.registerWatcher(deviceWatcher);
                }

                addDevice(devInfo.getSid(), device);
            } catch (DeviceNotSupported | GatewayNotFound | DeviceInitError e) {
                LOGGER.warning(e.getMessage());
            }
        }
    }

    private Class<?> getDriver(String driverName) throws DeviceNotSupported {
        if (!drivers.containsKey(driverName)) {
            try {
                StringBuilder fullDriverNamBuilder = new StringBuilder(driverPackage).append(".").append(driverName);
                Class<?> driver = Class.forName(fullDriverNamBuilder.toString());
                drivers.put(driverName, driver);
                return driver;
            } catch (ClassNotFoundException e) {
                throw new DeviceNotSupported(driverName);
            }
        }
        return drivers.get(driverName);
    }

    private BaseDevice initDevice(Class<?> driver, DeviceInfo deviceInfo) throws DeviceInitError, GatewayNotFound {
        try {
            Constructor<?>[] deviceConstructor = driver.getDeclaredConstructors();
            //TODO discover if nessesery
            if (deviceInfo.getArgs().containsKey("gateway")) {
                return (BaseDevice) deviceConstructor[0].newInstance(deviceInfo,
                        getGateway(deviceInfo.getArgs().get("gateway")));
            }
            return (BaseDevice) deviceConstructor[0].newInstance(deviceInfo);
        } catch (InstantiationException | IllegalAccessException | IllegalArgumentException
                | InvocationTargetException e) {
            throw new DeviceInitError(e.getMessage());
        }
    }

    private Gateway getGateway(String sid) throws GatewayNotFound {
        if (!this.devices.containsKey(sid)) {
            throw new GatewayNotFound(String.format("Gateway : %s not found", sid));
        }
        return (Gateway) this.devices.get(sid);
    }

    private synchronized void addDevice(String sid, BaseDevice device) {
        this.devices.put(sid, device);
    }

    public void update(StatusEvent statusEvent) {
        BaseDevice dev = this.devices.get(statusEvent.getSid());
        if (dev != null) {
            try {
                if (dev.status.update(statusEvent)) {
                    bus.dispatch(statusEvent);
                }
            } catch (AttributeReadOnly e) {
                LOGGER.warning(String.format("Attribute %s is readonly", statusEvent.getName()));
            }
        }
    }

    public void execute(String sid, String cmd, Object args) {
        if (this.devices.containsKey(sid)) {
            BaseDevice device = this.devices.get(sid);
            device.execute(cmd, args);
        }
    }

    public <T> T queryStatus(String sid, String attrName) {
        BaseDevice dev = devices.get(sid);
        T attr = dev.query(attrName);
        return attr;
    }

    public BaseDevice getDevice(String sid) {
        return devices.get(sid);
    }

    public EventBus getBus() {
        return this.bus;
    }

}
