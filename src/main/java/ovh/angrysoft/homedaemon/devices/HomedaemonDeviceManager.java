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
import java.util.Map.Entry;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;
import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import ovh.angrysoft.homedaemon.bus.Event;
import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.discover.DeviceDiscovery;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceInitError;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceNotSupported;
import ovh.angrysoft.homedaemon.exceptions.devices.GatewayNotFound;
import ovh.angrysoft.homedaemon.exceptions.discover.DeviceNotDiscovered;
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
    private DeviceDiscovery deviceDiscovery;
    private String driverPackage = "ovh.angrysoft.homedaemon.devices";

    public HomedaemonDeviceManager(String deviceInfoDir, EventBus bus) {
        this.deviceInfoDir = deviceInfoDir;
        this.devicesInfoList = new ArrayList<>();
        this.bus = bus;
        this.devices = new HashMap<>();
        this.drivers = new HashMap<>();
        this.watcherManager = new WatcherManager(this);
        this.deviceDiscovery = new DeviceDiscovery();
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
            return file.getName().endsWith(".json");
        })) {
            try {

                DeviceInfo deviceInfo =
                        new Gson().fromJson(new FileReader(devInfoFile), DeviceInfo.class);
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
                LOGGER.log(Level.SEVERE, "Device info file parse error: {0}",
                        devInfoFile.getName());
            } catch (VerifyError e) {
                LOGGER.log(Level.SEVERE, String.format("Device info file parse error: %s : %s",
                        devInfoFile.getName(), e.getMessage()));
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
        DeviceInfo clockInfo = new DeviceInfo("clock", "clock", "homedaemon", "clock", clockName,
                clockPlace, "software.ClockDevice", new HashMap<>());
        this.devicesInfoList.add(clockInfo);

        // State
        Map<String, String> stateName = new HashMap<>();
        stateName.put("pl", "Stan");
        stateName.put("en", "State");
        Map<String, String> statePlace = new HashMap<>();
        statePlace.put("pl", "Wszędzie");
        statePlace.put("en", "everywhere");
        DeviceInfo stateInfo = new DeviceInfo("state", "state", "homedaemon", "state", stateName,
                statePlace, "software.StateDevice", new HashMap<>());
        this.devicesInfoList.add(stateInfo);
    }

    public void setupDevices() {
        for (DeviceInfo devInfo : devicesInfoList) {
            LOGGER.log(Level.INFO, "load device: {0} model : {1}",
                    new Object[] {devInfo.getSid(), devInfo.getModel()});
            try {
                Class<?> driver = getDriver(devInfo.getDriver());
                BaseDevice device = initDevice(driver, devInfo);

                if (device.isDiscoverable() && device.getDiscoverEngine() != null) {
                    getDiscoveryInfo(devInfo, device);
                }

                if (device.isGatewayNeeded()) {
                    String gatewaySid = devInfo.getArgs().get("gateway");
                    device.setGateway(getGateway(gatewaySid));
                }

                device.setup();

                Watcher deviceWatcher = device.getWatcher();
                if (deviceWatcher != null)
                    watcherManager.registerWatcher(deviceWatcher);

                addDevice(devInfo.getSid(), device);

            } catch (DeviceNotSupported e) {
                LOGGER.warning(new StringBuilder("Device not supported - ").append(e.getMessage())
                        .toString());
            } catch (GatewayNotFound e) {
                LOGGER.warning(new StringBuilder("Gateway not found - ").append(e.getMessage())
                        .toString());
            } catch (DeviceNotDiscovered e) {
                LOGGER.warning(new StringBuilder("Device not Discovered - ")
                        .append(devInfo.getSid()).toString());
            } catch (DeviceInitError e) {
                LOGGER.warning(
                        new StringBuilder("Device Init - ").append(devInfo.getSid()).toString());
            }
        }

    }

    private void getDiscoveryInfo(DeviceInfo devInfo, BaseDevice device)
            throws DeviceNotDiscovered {
        Map<String, Object> discoveryInfo =
                deviceDiscovery.discover(devInfo.getSid(), device.getDiscoverEngine());
        for (Entry<String, Object> entry : discoveryInfo.entrySet()) {
            try {
                device.status.update(entry.getKey(), entry.getValue());
            } catch (AttributeReadOnly e) {
                LOGGER.warning(new StringBuilder("Attribute Read Only - ").append(devInfo.getSid())
                        .append(" - ").append(entry.getKey()).toString());

            }
        }
    }

    private Class<?> getDriver(String driverName) throws DeviceNotSupported {
        if (!drivers.containsKey(driverName)) {
            try {
                StringBuilder fullDriverNamBuilder =
                        new StringBuilder(driverPackage).append(".").append(driverName);
                Class<?> driver = Class.forName(fullDriverNamBuilder.toString());
                drivers.put(driverName, driver);
                return driver;
            } catch (ClassNotFoundException e) {
                throw new DeviceNotSupported(new StringBuilder(e.getMessage()).append(" ")
                        .append(driverName).toString());
            }
        }
        return drivers.get(driverName);
    }

    private BaseDevice initDevice(Class<?> driver, DeviceInfo deviceInfo) throws DeviceInitError {
        try {
            Constructor<?> deviceConstructor = driver.getConstructors()[0];
            return (BaseDevice) deviceConstructor.newInstance(deviceInfo);
        } catch (InstantiationException | IllegalAccessException | IllegalArgumentException
                | InvocationTargetException e) {
            e.printStackTrace();
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

    public void update(Event event) {
        if (!this.devices.containsKey(event.getSid()))
            return;
        BaseDevice dev = this.devices.get(event.getSid());
        try {
            if (dev.status.update(event.getName(), event.getValue())) {
                bus.dispatch(event);
            }
        } catch (AttributeReadOnly e) {
            LOGGER.warning(String.format("Attribute %s is readonly", event.getName()));
        }
    }

    public void execute(String sid, String cmd, Optional<Object> args) {
        if (this.devices.containsKey(sid)) {
            BaseDevice device = this.devices.get(sid);
            device.execute(cmd, args);
        }
    }

    public <T> T queryStatus(String sid, String attrName) {
        BaseDevice dev = devices.get(sid);
        return dev.query(attrName);
    }

    public BaseDevice getDevice(String sid) {
        return devices.get(sid);
    }

    public EventBus getBus() {
        return this.bus;
    }

    @Override
    public List<Map<String, Object>> getDevicesList() {
        List<Map<String, Object>> result = new ArrayList<>();
        for (Entry<String, BaseDevice> deviceEntry : devices.entrySet()) {
            result.add(deviceEntry.getValue().getDeviceStatus());
        }
        return result;
    }

}
