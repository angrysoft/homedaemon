package ovh.angrysoft.homedaemon.devices;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceNotSupported;
import ovh.angrysoft.homedaemon.exceptions.discover.DeviceNotDiscovered;
import ovh.angrysoft.homedaemon.watcher.WatcherManager;

public class DeviceManager {
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");
    private DeviceFactory deviceFactory;
    private String deviceInfoDir;
    private ArrayList<DeviceInfo> gatewaysInfoList;
    private ArrayList<DeviceInfo> devicesInfoList;
    private EventBus bus;
    private HashMap<String, BaseDevice> devices;

    public DeviceManager(String deviceInfoDir, EventBus bus) {
        this.deviceInfoDir = deviceInfoDir;
        this.gatewaysInfoList = new ArrayList<DeviceInfo>();
        this.devicesInfoList = new ArrayList<DeviceInfo>();
        this.bus = bus;
        this.deviceFactory = new DeviceFactory(new WatcherManager(this));
        this.devices = new HashMap<>();
    }

    public void loadDevice() {
        File devDir = new File(deviceInfoDir);
        if (!devDir.exists() && !devDir.isDirectory()) {
            LOGGER.log(Level.ALL, "Cannot access device dir : {0}", deviceInfoDir);
            return;
        }

        for (File devInfoFile : devDir.listFiles()) {
            if (!devInfoFile.getName().endsWith(".json"))
                continue;
            try {

                DeviceInfo deviceInfo = new Gson().fromJson(new FileReader(devInfoFile), DeviceInfo.class);
                if (deviceInfo.type != null && deviceInfo.type.equals("gateway")) {
                    gatewaysInfoList.add(deviceInfo);
                } else {
                    devicesInfoList.add(deviceInfo);
                }

            } catch (FileNotFoundException e) {
                LOGGER.log(Level.ALL, "Device info file {0} not found", devInfoFile.getName());
            } catch (JsonSyntaxException e) {
                LOGGER.log(Level.ALL, "Device info file parse error: {0}", devInfoFile.getName());
            }
        }
    }

    public void setup() {
        setupGateways();
        setupDevices();
    }

    private void setupGateways() {
        for (DeviceInfo gatewayInfo : gatewaysInfoList) {
            LOGGER.log(Level.INFO, "load gateway: {0}", gatewayInfo.sid);
        }

    }

    private void setupDevices() {
        for (DeviceInfo devInfo : devicesInfoList) {
            LOGGER.log(Level.INFO, "load device: {0}", devInfo.sid);
            try {
                BaseDevice device = deviceFactory.getDevice(devInfo);
                addDevice(devInfo.sid, device);
            } catch (DeviceNotSupported e) {
                LOGGER.warning(e.getMessage());
            } catch (DeviceNotDiscovered e) {
                LOGGER.warning(e.getMessage());
            }
        }
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

}
